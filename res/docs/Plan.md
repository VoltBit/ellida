* Ce este parctic framework-ul? Este un layer de Yocto? Este un set de scripturi organizat într-o aplicație?


Cerințe
[1] Yocto project
Care va fi inputul?
[*] Cum arată receipe și layer? Cum se folosesc?
[*] Ce de fapt poky?



[2] Extensibility


[3] Remote execution


[4] Linux testing suites


[5] Testing formats for CGL and AGL


[6] Perfomance

[**] Mod de testare
- Framework-ul trebuie să fie scalabil, pot fi testate în paralel oricât de multe detalii ale specificației. Trebuie să poată fi specificat ce test este standalone și ce test este independent de instanța de VM în care rulează (dacă este nevoie să fie spawnată o noua VM sau nu).
- Sistem de conflicte între teste, evitată introducerea de zgomot.

1) Sunt analizate testele cerute și resursele sistemului
2) Este determinată o ordonare optimă a testelor, unele teste au nevoie de mai multe threaduri, de mult IO sau CPU
3) Sunt executați pașii și este dat feedback în timp real
4) Testarea ar trebuii să poată fi abandonată într-un mod curat în orice moment

[**] Organizarea testelor
 - Fișier de configurare JSON unde sunt specificate testele și informațiile necesare: resurse de care depinde, independență de comportamentul sistemului, prioritate

https://github.com/SUPERAndroidAnalyzer/super/blob/master/rules.json


## Tipurile de teste și modul de implementare