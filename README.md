# Matematikai modellek 1-2.

A kurzus célja, hogy a hallgatókat már a képzés első évében bevezesse a Python programozási nyelv használatába matematikai és adat-alapú problémák megoldásán keresztül.

## Teendők a projekt klónozásakor

- A projekt klónozásához bemutató videó elérhető a Coospace-en (_git_clone.mkv_).
- Ha a repository-t frissen klónozzuk ki, akkor
  - Amikor a Kalmár kabinetben először klónozunk, nyissuk meg a terminált, majd futtassuk a következő parancsokat:
      
      `git config --global --unset user.name`
      
      `git config --global --unset user.email`.
    
      Ezen parancsok futtattásával azt érjük el, hogy a korábban előttünk ugyanazon gépen dolgozó hallgató Git-es adatai elvetésre kerüljenek.
  
  
  - A saját adataink beállítására:

      `git config --local user.name "NÉV"`
      
      `git config --local user.email "EMAIL"`
    
      Utóbbi két parancs biztosítja, hogy a commitok során a saját adataink jelenjenek meg.

  - A `gitconfig-special` fájlba írjuk bele az előző blokkban említett parancsoknál megadott adatainkat.

  - PyCharm-ban a következő módon hozhatunk létre virtuális környezetet: 
    
      **File -> Settings -> Project: "<név>"-matmod-2024 -> Python Interpreter -> Add Interpreter -> Add Local Interpreter -> OK**
    
      Ekkor a folyamat végén egy új mappa fog megjelenni a projekt oldalsávban, aminek neve: `venv`.
