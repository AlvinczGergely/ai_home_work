# AI-alapú Pong Játék Evolúció Beadando

## Projekt Áttekintés

Ez a projekt több lépésben készült, kezdve egy alap Pong játékkal, majd AI-alapú játékosok beépítésével, akik evolúciós algoritmusok segítségével versenyeznek egymással. A cél az, hogy több AI-t képezzünk ki Pong játékra, és evolúciós algoritmus segítségével optimalizáljuk teljesítményüket, majd versenyeztessük őket egymás ellen.

## 0. lépés: Alap Pong Játék

A projekt kezdeti lépésében egy alap Pong játékot fejlesztettem Python és Pygame könyvtár segítségével. A játékban egy felhasználó által irányított játékos és egy számítógép vezérelte ellenfél szerepel. A labda visszapattan a felső és alsó falról, és a játékosoknak el kell találniuk a labdát a pálcájukkal, hogy megakadályozzák annak elhúzását.

Főbb jellemzők:
- Egyszerű Pong játék logika alapvető vezérlésekkel
- Játékos általi vezérles (kesobb ai)
- Számítógép vezérelte ellenfél

## 1. lépés: Irodalomkutatás

A második lépésben irodalomkutatást végeztem két fő területen: AI  megerősítéses tanulás, és evolúciós algoritmusok.

1. **Megerősítéses Tanulás**:
   - A megerősítéses tanulás egy gépi tanulási módszer, amelyben az ügynökök (tanulnak, hogyan viselkedjenek egy környezetben, például egy játékban, cselekvések végrehajtásával és visszajelzéseken keresztül.
   - A Pong játék esetében az AI ügynökök a pálca helyzetét tanulják meg a labda mozgása alapján, és próbálnak optimalizálni a teljesítményükön úgy, hogy minimalizálják az ellenfél által szerzett pontokat.

2. **Evolúciós Algoritmusok**:
   - Az evolúciós algoritmusok optimalizációs technikák, amelyek a természetes szelekció folyamatát modellezik. Különösen hasznosak olyan problémák esetén, ahol a megoldás tér túl nagy vagy komplex ahhoz, hogy hagyományos optimalizációs módszerekkel kezeljük.

## 2. lépés: AI Képzés és Evolúció

### 2.1 Config file
   ### [Neat]
      1. fitness_criterion: kritirium ertek(jelen allapotban max)
      2. fitness_threshold: amint elerjuk az erteket az adott tanitas megall
      3. pop_size: egyedek szama generacioneknt
      4. reset_on_extrapolation: 
   ### [DefaultGenome]
      1. num_inputs: bemenetek szama(lambda_x, labda_y, uto_y)
      2. num_outputs: amit az ai tanul(mozgas y+, y-)
      3. num_hidden: rejtett nodok szama(ha nulla miert kell megadni?)
      4. feed_forward: ha true akkor a generalt halo nem lehet ujrakapacsolatos
      5. initial_connection: ujjonan letrejovo genomok kapcsolodasa(full->nics hidden nodom szoval nem fog jelezni)

   #### Activation
      6. activation_default: alapertelmezett aktivacios fuggveny parameter, alapbol random
      7. activation_mutate_rate: valszinusege, hogy mutacio lecsereli az aktivacios fuggvenyt erteket randomra
      8. activation_options: csomopontok altal hasznalhato aktivacios fuggvenyt szspace-el elvalasztott listaja????

   #### Node Bias
      9. bias_init_stdev: gauss eloszlas erteke uj csomopontok kivalasztasahoz
      10. bias_mutate_rate: valoszinusege a mutacionak random ertek szerinte
      11. bias_replace_rate: valoszinusege a mutacio cserenek random ertek szerinte

   #### Connection Weights
      12. weight_init_stdev: uj kapcsolatokhoz hasznalt disztribucio gausz eloszlasnal
      13. weight_mutate_rate: valoszinusege a mutacio soran suly valtozasnak

   #### Structural Mutation
      14. conn_add_prob: eselye a kapcsolatnak mutacio kozben(1 es1 kozott, 0.5 lett random)
      15. conn_delete_prob: kapcsoalt torlese mutacio sora (1 es1 kozott, 0.5 lett random)
      16. enabled_default: ujjonan letrejovo kapcsolatok engedejezese(jelen esetben true)

   ### [DefaultSpeciesSet]
      1. compatibility_threshold = fajhoz sorolas genomialis ertek alapjan ????

   ### [DefaultStagnation]
      1. species_fitness_func: egyedek fittnes meresere hasznalt fuggveny(alapbol "mean")
      2. max_stagnation: kuszobertek, ha elerjuk es nem fejlodott egy csalad elkaszaljuk az egeszet

   ### [DefaultReproduction]
      1. elitism: legfitteb egyedek szama amiket megtartunk kovetlkezo generaciora
      2. survival_threshold: fajok hanyada amiket engedunk szaporodni generacionkent