/*
 * ddsolve.c - a small double-dummy solver for the JBF results archive.
 *
 * Reads deals from stdin, one per line:
 *     <id> <N> <E> <S> <W>
 * where each hand is "spades.hearts.diamonds.clubs" with ranks AKQJT98765432
 * (an empty suit is written as nothing between the dots).
 * Writes one line per deal:
 *     <id> <20 numbers>
 * the tricks the declarer takes with best play by all four players, ordered
 * by strain (NT, S, H, D, C) and, within each strain, declarer (N, E, S, W).
 *
 * Method: alpha-beta search over complete tricks with a transposition table
 * keyed on the relative-rank layout of the remaining cards at each trick
 * boundary, equivalent-card pruning and simple move ordering.
 *
 * Build: cc -O2 -o ddsolve ddsolve.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define NT 4
#ifndef EXACT_DEPTH
#define EXACT_DEPTH 5
#endif
static int trump;                 /* 0..3 = S,H,D,C ; 4 = notrump          */
static uint16_t hand[4][4];       /* [player][suit] bitmask, bit r = rank r (0=2 .. 12=A) */

/* ---------- transposition table ---------- */
typedef struct { uint64_t k1, k2; int8_t lb, ub; int8_t bs, br; uint16_t gen; } TTE;
#define TTBITS 24
static uint16_t curgen = 1;
#define TTSIZE (1u << TTBITS)
static TTE *tt;

static uint64_t mix(uint64_t x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL; x ^= x >> 33; return x; }

/* relative layout: for each suit, owners of the remaining cards from the top */
static void make_key(int leader, uint64_t *k1, uint64_t *k2)
{
    uint64_t part[4];
    for (int s = 0; s < 4; s++) {
        uint64_t v = 0; int n = 0;
        for (int r = 12; r >= 0; r--) {
            uint16_t b = 1u << r;
            for (int p = 0; p < 4; p++) if (hand[p][s] & b) { v = (v << 2) | p; n++; break; }
        }
        part[s] = (v << 4) | n;          /* <= 26 + 4 bits */
    }
    *k1 = part[0] | (part[1] << 30);
    *k2 = part[2] | (part[3] << 30) | ((uint64_t)leader << 60);
}

static TTE *tt_find(uint64_t k1, uint64_t k2, int create)
{
    uint64_t h = mix(k1 ^ mix(k2)) & (TTSIZE - 1);
    for (int i = 0; i < 16; i++) {
        TTE *e = &tt[(h + i) & (TTSIZE - 1)];
        if (e->gen != curgen) { if (!create) return NULL; e->gen = curgen; e->k1 = k1; e->k2 = k2; e->lb = 0; e->ub = 13; e->bs = -1; return e; }
        if (e->k1 == k1 && e->k2 == k2) return e;
    }
    if (!create) return NULL;
    TTE *e = &tt[h]; e->gen = curgen; e->k1 = k1; e->k2 = k2; e->lb = 0; e->ub = 13; e->bs = -1; return e;
}

/* ---------- search ---------- */
typedef struct { int suit, rank; } Card;

static int highest(uint16_t m) { return 31 - __builtin_clz((unsigned)m); }
static int lowest(uint16_t m) { return __builtin_ctz((unsigned)m); }

/* generate one representative per run of equivalent cards for player p */
static int gen_moves(int p, int led, Card *out)
{
    int n = 0;
    uint16_t all[4];
    for (int s = 0; s < 4; s++) all[s] = hand[0][s] | hand[1][s] | hand[2][s] | hand[3][s];
    int canfollow = (led >= 0 && hand[p][led]);
    for (int s = 0; s < 4; s++) {
        if (canfollow && s != led) continue;
        uint16_t m = hand[p][s];
        if (!m) continue;
        int prev_in_run = 0;
        for (int r = 12; r >= 0; r--) {
            uint16_t b = 1u << r;
            if (!(all[s] & b)) continue;               /* played: skip, runs continue across gaps */
            if (m & b) {
                if (!prev_in_run) { out[n].suit = s; out[n].rank = r; n++; }
                prev_in_run = 1;
            } else prev_in_run = 0;
        }
    }
    return n;
}

static int beats(Card a, Card b, int led)   /* does a beat b (b is current winner) */
{
    if (a.suit == b.suit) return a.rank > b.rank;
    if (trump != NT && a.suit == trump) return 1;
    (void)led;
    return 0;
}

static long nodes;

/* sure tricks the side on lead can cash at once: leader's own cards that are
   higher than every opponent card in the suit (and cannot be ruffed) */
static int qt_from(int leader, int *cross)
{
    int lho = (leader + 1) & 3, rho = (leader + 3) & 3, pard = (leader + 2) & 3;
    int opp_trumps = (trump != NT) && (hand[lho][trump] | hand[rho][trump]);
    int q = 0;
    for (int s = 0; s < 4; s++) {
        uint16_t L = hand[leader][s];
        cross[s] = 0;
        if (!L) continue;
        uint16_t O = hand[lho][s] | hand[rho][s];
        int lim = 13;
        if (s != trump && opp_trumps) {
            if ((!hand[lho][s] && hand[lho][trump]) || (!hand[rho][s] && hand[rho][trump])) lim = 0;
            else {
                int cl = __builtin_popcount(hand[lho][s]), cr = __builtin_popcount(hand[rho][s]);
                lim = cl < cr ? cl : cr;
            }
        }
        int cnt = O ? __builtin_popcount(L >> (highest(O) + 1)) : __builtin_popcount(L);
        if (cnt > lim) cnt = lim;
        q += cnt;
        /* can the lead in s reach partner's sure winner? */
        uint16_t P = hand[pard][s];
        if (P && lim > 0 && (!O || highest(P) > highest(O))) cross[s] = 1;
    }
    return q;
}

static int quick_tricks(int leader)
{
    int cl[4], cp[4];
    int ql = qt_from(leader, cl);
    int pard = (leader + 2) & 3;
    int any = 0;
    for (int s = 0; s < 4; s++) if (cl[s]) any = 1;
    if (!any) return ql;
    int qp = qt_from(pard, cp);
    return qp > ql ? qp : ql;
}


/* order moves in-place: rough heuristics */
static void order_moves(int p, int pos, Card *mv, int n, Card *trick, int winner_pos, int led)
{
    int score[64];
    for (int i = 0; i < n; i++) {
        int sc = 0; Card c = mv[i];
        if (pos == 0) {
            uint16_t all = hand[0][c.suit] | hand[1][c.suit] | hand[2][c.suit] | hand[3][c.suit];
            int top = highest(all);
            int partner = (p + 2) & 3;
            if (c.rank == top) sc += 50;
            else if (hand[partner][c.suit] && highest(hand[partner][c.suit]) == top) sc += 40 - c.rank;
            else sc += 10 - c.rank;
            if (trump != NT && c.suit == trump) sc -= 5;
        } else {
            Card w = trick[winner_pos];
            int partner_winning = ((winner_pos ^ pos) & 1) == 0;   /* positions 0/2 vs 1/3 */
            int wins = beats(c, w, led);
            if (partner_winning) sc = 30 - c.rank - (trump != NT && c.suit == trump && c.suit != led ? 20 : 0);
            else if (wins) sc = 60 - c.rank - (trump != NT && c.suit == trump && c.suit != led ? 5 : 0);
            else sc = 20 - c.rank;
            if (pos == 1 && c.suit == led && !wins) sc += 5;
        }
        score[i] = sc;
    }
    for (int i = 1; i < n; i++) {      /* insertion sort, descending */
        Card c = mv[i]; int s = score[i], j = i - 1;
        while (j >= 0 && score[j] < s) { mv[j + 1] = mv[j]; score[j + 1] = score[j]; j--; }
        mv[j + 1] = c; score[j + 1] = s;
    }
}

/* returns NS tricks from the remaining cards; leader leads the next trick */
static int search(int leader, int remaining, int alpha, int beta);

static Card g_best_lead; static int g_hint_s = -1, g_hint_r = -1;
static int play_trick(int leader, int remaining, int pos, Card *trick, int winner_pos, int alpha, int beta)
{
    if (pos == 4) {
        int winner = (leader + winner_pos) & 3;
        int ns = (winner & 1) == 0;
        return ns + search(winner, remaining - 1, alpha - ns, beta - ns);
    }
    int p = (leader + pos) & 3;
    int led = pos ? trick[0].suit : -1;
    Card mv[52];
    int n = gen_moves(p, led, mv);
    order_moves(p, pos, mv, n, trick, winner_pos, led);
    if (pos == 0 && g_hint_s >= 0) {
        for (int i = 0; i < n; i++) if (mv[i].suit == g_hint_s && mv[i].rank == g_hint_r) { Card t = mv[i]; for (int j = i; j > 0; j--) mv[j] = mv[j-1]; mv[0] = t; break; }
        g_hint_s = -1;
    }
    Card bestc = mv[0];
    int maxing = (p & 1) == 0;
    int best = maxing ? -1 : 99;
    for (int i = 0; i < n; i++) {
        Card c = mv[i];
        hand[p][c.suit] &= ~(1u << c.rank);
        trick[pos] = c;
        int wp = (pos == 0 || beats(c, trick[winner_pos], led)) ? pos : winner_pos;
        int v = play_trick(leader, remaining, pos + 1, trick, wp, alpha, beta);
        hand[p][c.suit] |= (1u << c.rank);
        if (maxing) { if (v > best) { best = v; bestc = c; } if (best > alpha) alpha = best; }
        else        { if (v < best) { best = v; bestc = c; } if (best < beta) beta = best; }
        if (alpha >= beta) break;
    }
    if (pos == 0) g_best_lead = bestc;
    return best;
}

/* quick bounds: tricks the side on lead can cash from the top in NT / with no trumps out */
static int search(int leader, int remaining, int alpha, int beta)
{
    nodes++;
    if (remaining == 0) return 0;
    if (alpha >= remaining) return remaining;   /* cannot exceed */
    if (beta <= 0) return 0;
    {
        int q = quick_tricks(leader);
        if (q > remaining) q = remaining;
        if ((leader & 1) == 0) { if (q >= beta) return q; }
        else { if (remaining - q <= alpha) return remaining - q; }
    }
    uint64_t k1, k2;
    make_key(leader, &k1, &k2);
    TTE *e = tt_find(k1, k2, 0);
    if (e) {
        if (e->lb >= beta) return e->lb;
        if (e->ub <= alpha) return e->ub;
        if (e->lb == e->ub) return e->lb;
        if (e->lb > alpha) alpha = e->lb;
        if (e->ub < beta) beta = e->ub;
    }
    if (remaining <= EXACT_DEPTH) { alpha = -1; beta = remaining + 1; }   /* small endgames: solve exactly once */
    int a0 = alpha, b0 = beta;
    Card trick[4];
    if (e && e->bs >= 0) { g_hint_s = e->bs; g_hint_r = e->br; }
    int v = play_trick(leader, remaining, 0, trick, 0, alpha, beta);
    Card bl = g_best_lead;
    e = tt_find(k1, k2, 1);
    e->bs = bl.suit; e->br = bl.rank;
    if (v <= a0) { if (v < e->ub) e->ub = v; }
    else if (v >= b0) { if (v > e->lb) e->lb = v; }
    else { e->lb = e->ub = v; }
    if (e->ub > remaining) e->ub = remaining;
    return v;
}

/* exact NS tricks via null-window probes (MTD-like) */
static int solve_ns(int leader, int guess)
{
    int lo = 0, hi = 13;
    int t = guess < 1 ? 1 : (guess > 13 ? 13 : guess);
    while (lo < hi) {
        if (t <= lo) t = lo + 1;
        if (t > hi) t = hi;
        int v = search(leader, 13, t - 1, t);
        if (v >= t) { lo = t; t = t + 1; } else { hi = t - 1; t = t - 1; }
        if (lo < hi && (t <= lo || t > hi)) t = (lo + hi + 1) / 2;
    }
    return lo;
}

static int parse_hand(const char *s, int p)
{
    int suit = 0, cnt = 0;
    for (; *s && suit < 4; s++) {
        if (*s == '.') { suit++; continue; }
        const char *R = "23456789TJQKA";
        const char *q = strchr(R, *s);
        if (!q) return -1;
        hand[p][suit] |= 1u << (q - R);
        cnt++;
    }
    return cnt;
}

int main(void)
{
    tt = calloc(TTSIZE, sizeof(TTE));
    if (!tt) return 1;
    char id[128], h[4][64];
    static const int strain_order[5] = { NT, 0, 1, 2, 3 };
    while (scanf("%127s %63s %63s %63s %63s", id, h[0], h[1], h[2], h[3]) == 5) {
        memset(hand, 0, sizeof hand);
        int ok = 1, tot = 0;
        for (int p = 0; p < 4; p++) { int c = parse_hand(h[p], p); if (c != 13) ok = 0; tot += c; }
        if (!ok) { printf("%s ERR\n", id); fflush(stdout); continue; }
        printf("%s", id);
        for (int si = 0; si < 5; si++) {
            trump = strain_order[si];
            curgen++;
            int guess = 7;
            for (int decl = 0; decl < 4; decl++) {
                int leader = (decl + 1) & 3;
                int ns = solve_ns(leader, guess);
                guess = ns;
                printf(" %d", (decl & 1) == 0 ? ns : 13 - ns);
            }
        }
        printf("\n");
        fprintf(stderr, "%s nodes=%ld\n", id, nodes); nodes = 0;
        fflush(stdout);
    }
    return 0;
}
