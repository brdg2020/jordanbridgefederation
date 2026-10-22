# Double-dummy analysis

`dds_results.jsonl.gz` holds one line per distinct deal in the results archive:
the double-dummy table (tricks for each strain and declarer), the dealer par score
and contracts, and the tricks the declarer takes after every opening lead.

It was produced with the open-source DDS solver (https://github.com/dds-bridge/dds,
Apache-2.0) through `driver.cpp`:

    # build DDS's library/src/*.cpp into object files, then
    g++ -O2 -std=c++20 -pthread -I<dds>/library/src -I<dds>/library driver.cpp <objects> -o ddsdrv
    # input lines: "<id> <dealer> <vul> <N> <E> <S> <W>" with hands written as S.H.D.C
    ./ddsdrv < deals.txt > out.jsonl

`tools/build_results_extras.py` merges the file into `public/data/results/events/*.json`
and checks it against the makeable contracts Bridgewebs published (no mismatches).

`ddsolve.c` is a small independent solver written while setting this up; it agrees
with DDS but is far slower, so it is kept only as a cross-check.
