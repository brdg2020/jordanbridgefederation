// Driver: reads "<id> <dealer N/E/S/W> <vul None/NS/EW/All> N E S W" lines (hands as S.H.D.C),
// prints JSON per line: DD table (tricks, strains NT S H D C x declarers N E S W),
// dealer par score/contracts, and opening-lead tricks for each strain/declarer.
#include <cstdio>
#include <cstring>
#include <string>
#include <cstdlib>
#include <api/dll.h>
static const char *SU = "SHDC";
static const char *RK = "  23456789TJQKA";
int main() {
  char id[64], dl[8], vl[8], h[4][40];
  while (scanf("%63s %7s %7s %39s %39s %39s %39s", id, dl, vl, h[0], h[1], h[2], h[3]) == 7) {
    DdTableDealPBN d; snprintf(d.cards, sizeof d.cards, "N:%s %s %s %s", h[0], h[1], h[2], h[3]);
    DdTableResults r;
    int rc = CalcDDtablePBN(d, &r);
    if (rc != 1) { printf("{\"id\":\"%s\",\"err\":%d}\n", id, rc); continue; }
    int dealer = strchr("NESW", dl[0]) - "NESW";
    int vul = !strcmp(vl,"None")?0: !strcmp(vl,"All")?1: !strcmp(vl,"NS")?2:3;
    ParResultsDealer pd; DealerPar(&r, &pd, dealer, vul);
    printf("{\"id\":\"%s\",\"dd\":[", id);
    int sord[5] = {4,0,1,2,3}; // NT S H D C -> DDS strain index (S=0,H=1,D=2,C=3,NT=4)
    for (int si = 0; si < 5; si++) { printf(si?",[":"["); for (int p = 0; p < 4; p++) printf(p?",%d":"%d", r.res_table[sord[si]][p]); printf("]"); }
    printf("],\"par\":%d,\"parc\":[", pd.score);
    for (int i = 0; i < pd.number; i++) printf(i?",\"%s\"":"\"%s\"", pd.contracts[i]);
    if (getenv("NOLEADS")) { printf("]}\n"); fflush(stdout); continue; }
    printf("],\"leads\":[");
    for (int si = 0; si < 5; si++) {
      printf(si?",[":"[");
      for (int decl = 0; decl < 4; decl++) {
        DealPBN dp; memset(&dp, 0, sizeof dp);
        dp.trump = sord[si]; dp.first = (decl + 1) % 4;
        snprintf(dp.remainCards, sizeof dp.remainCards, "N:%s %s %s %s", h[0], h[1], h[2], h[3]);
        FutureTricks ft; memset(&ft, 0, sizeof ft);
        int rr = SolveBoardPBN(dp, -1, 3, 1, &ft, 0);
        printf(decl?",\"":"\"");
        if (rr == 1) for (int i = 0; i < ft.cards; i++) {
          // card and equals (lower equivalent cards in same suit), tricks for declarer side
          std::string cards; cards += SU[ft.suit[i]]; cards += RK[ft.rank[i]];
          for (int k = 2; k <= 14; k++) if (ft.equals[i] & (1 << k)) { cards += SU[ft.suit[i]]; cards += RK[k]; }
          printf("%s%s:%d", i?" ":"", cards.c_str(), 13 - ft.score[i]);
        }
        printf("\"");
      }
      printf("]");
    }
    printf("]}\n");
    fflush(stdout);
  }
}
