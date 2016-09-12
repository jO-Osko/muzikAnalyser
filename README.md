## Analiza ponavljajočih se sklad na storitvi Strudl Muzik

V tem projektu bom analiziral povaljajoče se sklade na spletni strani [muzik.si](http://muzik.si)
Muzik je servis, ki poslušalcem omogoča da brezplačno (in skoraj legalno) poslušajo glasbo, ki je dostopna na svetovnem spletu, tako da jo združi v skupno bazo, po kateri omogoča iskanje.
Ker je seveda s takim načinom dela ogromno pesmi podvojenih (ali poštirinajsterjenih) se je pojavil problem ponavljanja pesmi v iskalniku, kar je za uporabnike zelo moteče, saj ob iskanju dobimo voliko nepotrebnih rezultatov.
Muzik si seveda želi, da bi te rezultate združil in izmed enakih pesmi pokazal samo najkvalitenejšo oziroma s pomočjo pametnega algoritma razporedil uporabo na različne lokacije iste pesmi.

### Način dela
Od ustvarjalcev platforme sem pridobil originalno sqlite bazo prejšnje verzije projekta (baza ima sicer manjšo napako), ki sem jo nato izvozil v csv datoteko (med izvozom sem uredil tudi kodiranje znakov, saj del sklad prihaja iz ruskih strežnikov in je bilo v bazi nekaj problemov s kodnimi tabelami).
Csv datotke sem nato uvozil in iz njih naredil objekte, ter posamezni pesmi priredil kanonično ime (spremenil čžšćđ... v angleške podobne črke, odstranil posebne znake, odstranil avtorje, in razdelil naslov po besedah). 
Tako kanonizirane skladbe sem potem dal v skupine glede na enakost kanoničnega imena.

### Zajeti podatki
 
Ker je vseh pesmi preveč (malo čez 6,000,000) sem se odločil, da sem bom omejil samo na del serverjev (po dogovoru z muzik ekipo na tiste, ki so najbolj obiskani)
 
 
#### Tabela zajetih podatkov

| Ime v bazi    | Ime v modelu  | Opis                                                      |
| ------------- | ------------- | --------------------------------------------------------- |
| id            | muzik_id      | Muzik id pesmi (id s katero muzik identificira pesem)     |
| name          | name          | Naslov pesmi                                              |
| server        | server        | Id serverja, ki gostuje pesem                             |
| bitr          | bit_rate      | Bitna hitrost (naše osnovno merilo za kvaliteto pesmi)    |
| time          | duration      | Dolžina pesmi (v s)                                       |
| size          | size          | Velikost datoteke (v B)                                   |
| freq          | frequency     | Frekvenca zajemanja                                       |
| N/A           | canonic_name  | Kanonično ime                                             |


### Predvidena analiza

Namen analize je ovrednotiti kvaliteto iste pesmi na več različnih strežnikih in ugotoviti, kdo izmed teh ponuja najboljšo kvaliteto

* Pri posamezni ponavljajoči pesmi bomo pogledali, kateri izmed strežnikov jo ponuja pri največji bitni hitrosti (Osnovno merilo za določanje kvalitete)

[//]: # (Pogledali si bomo tudi velikost datoteke pri posamezni bitni hitrosti. Če je velikost datoteke pri večji bitni hitrosti primerljiva z velikostjo pri veliko manjši bitni hitrosti (320 <-> 256 <-> 192 <-> 128 ...), to lahko nakazuje na nesmiselnost večje številke, saj se pogosto dogaja da ve želji po navidezno bolj kvalitetni glasbi datoteke prekodiramo iz manjše v večjo bitno hitrost, a to ne nadomesti izgubljenih podatkov pri kodiranju na manjšo bitno hitrost že prej (MP3 standard za stiskanje podatkov z izgubo))