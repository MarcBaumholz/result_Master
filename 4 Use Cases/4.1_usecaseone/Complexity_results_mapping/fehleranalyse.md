# Fehleranalyse der Tabellen in ergebnisse.md

## Zusammenfassung

Die ursprünglichen Tabellen in `ergebnisse.md` enthielten **signifikante Abweichungen** von den tatsächlichen Ergebnissen aus den JSON-Dateien. Hier ist eine detaillierte Aufschlüsselung der gefundenen Fehler:

---

## 1. Single-Prompt Ergebnisse (Tabelle 1)

### Fehler in der ursprünglichen Tabelle:

| API | Original TP | Original FP | Original FN | Original TN | Korrigiert TP | Korrigiert FP | Korrigiert FN | Korrigiert TN |
|-----|-------------|-------------|-------------|-------------|---------------|---------------|---------------|---------------|
| **Flip** | **10** | **0** | **0** | **0** | **9** | **1** | **1** | **0** |
| **ADB** | **4** | **0** | **6** | **0** | **0** | **0** | **0** | **0** |
| **HiBob** | **9** | **1** | **0** | **0** | **7** | **1** | **3** | **0** |
| **Oracle** | **8** | **0** | **2** | **0** | **7** | **1** | **2** | **1** |
| **Personio** | **7** | **0** | **3** | **0** | **6** | **1** | **3** | **1** |
| **Rippling** | **9** | **1** | **0** | **0** | **9** | **1** | **1** | **0** |
| **Sage** | **8** | **0** | **2** | **0** | **7** | **1** | **3** | **0** |
| **Stackone** | **10** | **0** | **0** | **0** | **9** | **1** | **1** | **0** |
| **Workday** | **6** | **0** | **4** | **0** | **4** | **1** | **6** | **0** |

### Gesamtwerte Single-Prompt:
- **Original**: Precision 98.2%, Recall 73.7%, F1-Score 84.0%
- **Korrigiert**: Precision **89.2%**, Recall **68.0%**, F1-Score **77.2%**
- **Differenz**: -9.0% Precision, -5.7% Recall, -6.8% F1-Score

**Problem**: Die ursprünglichen Werte waren **zu optimistisch**. Mehrere APIs (Flip, ADB, HiBob, Oracle, Personio, Sage, Stackone, Workday) hatten fehlerhafte TP/FP/FN-Werte.

---

## 2. Basic RAG Ergebnisse (Tabelle 2)

### Fehler in der ursprünglichen Tabelle:

| API | Original TP | Original FP | Original FN | Original TN | Korrigiert TP | Korrigiert FP | Korrigiert FN | Korrigiert TN |
|-----|-------------|-------------|-------------|-------------|---------------|---------------|---------------|---------------|
| **Flip** | **10** | **0** | **0** | **0** | **9** | **1** | **1** | **0** |
| **ADB** | **7** | **2** | **1** | **0** | **9** | **1** | **1** | **0** |
| **BambooHR** | **9** | **1** | **0** | **0** | **10** | **0** | **0** | **1** |
| **HiBob** | **7** | **2** | **1** | **0** | **9** | **1** | **1** | **0** |
| **Oracle** | **8** | **1** | **0** | **1** | **8** | **2** | **1** | **0** |
| **Personio** | **7** | **2** | **1** | **0** | **8** | **2** | **1** | **0** |
| **Stackone** | **8** | **1** | **1** | **0** | **9** | **1** | **1** | **0** |
| **Workday** | **6** | **2** | **2** | **0** | **9** | **1** | **1** | **0** |

### Gesamtwerte Basic RAG:
- **Original**: Precision 85.0%, Recall 92.3%, F1-Score 88.4%
- **Korrigiert**: Precision **88.2%**, Recall **90.7%**, F1-Score **89.4%**
- **Differenz**: +3.2% Precision, -1.6% Recall, +1.0% F1-Score

**Problem**: Die ursprünglichen Recall-Werte waren **überschätzt**, aber die Precision war **unterschätzt**.

---

## 3. Enhanced RAG Ergebnisse (Tabelle 3)

### Fehler in der ursprünglichen Tabelle:

| API | Original TP | Original FP | Original FN | Original TN | Korrigiert TP | Korrigiert FP | Korrigiert FN | Korrigiert TN |
|-----|-------------|-------------|-------------|-------------|---------------|---------------|---------------|---------------|
| **Flip** | **10** | **0** | **0** | **0** | **0** | **10** | **10** | **1** |
| **ADB** | **7** | **3** | **0** | **0** | **9** | **1** | **1** | **0** |
| **BambooHR** | **9** | **0** | **1** | **0** | **10** | **0** | **0** | **1** |
| **HiBob** | **10** | **0** | **0** | **0** | **9** | **1** | **1** | **0** |
| **Oracle** | **9** | **1** | **0** | **0** | **8** | **2** | **1** | **0** |
| **Personio** | **7** | **0** | **0** | **3** | **6** | **1** | **3** | **1** |
| **Rippling** | **10** | **0** | **0** | **0** | **9** | **1** | **1** | **0** |
| **Sage** | **9** | **1** | **0** | **0** | **9** | **1** | **1** | **0** |
| **SAP** | **5** | **5** | **0** | **0** | **8** | **2** | **1** | **0** |
| **Stackone** | **10** | **0** | **0** | **0** | **9** | **1** | **1** | **0** |
| **Workday** | **7** | **0** | **1** | **2** | **6** | **1** | **4** | **0** |

### Gesamtwerte Enhanced RAG:
- **Original**: Precision 90.9%, Recall 98.0%, F1-Score 93.3%
- **Korrigiert**: Precision **79.8%**, Recall **77.6%**, F1-Score **78.7%**
- **Differenz**: -11.1% Precision, -20.4% Recall, -14.6% F1-Score

**Problem**: Die ursprünglichen Werte waren **massiv überschätzt**. Dies ist der größte Fehler in allen Tabellen.

**Kritischer Fehler**: Die Flip-Ergebnisse waren komplett falsch (sollte 0/10/10/1 sein, nicht 10/0/0/0).

---

## 4. Complete Architecture Ergebnisse (Tabelle 4)

### Fehler in der ursprünglichen Tabelle:

| API | Original TP | Original FP | Original FN | Original TN | Korrigiert TP | Korrigiert FP | Korrigiert FN | Korrigiert TN |
|-----|-------------|-------------|-------------|-------------|---------------|---------------|---------------|---------------|
| **Flip** | **10** | **0** | **0** | **0** | **0** | **0** | **0** | **0** |
| **ADB** | **10** | **0** | **0** | **0** | **3** | **1** | **7** | **0** |
| **BambooHR** | **9** | **1** | **0** | **0** | **10** | **0** | **0** | **1** |
| **HiBob** | **10** | **0** | **0** | **0** | **9** | **1** | **1** | **0** |
| **Oracle** | **10** | **0** | **0** | **0** | **8** | **2** | **1** | **0** |
| **Personio** | **9** | **1** | **0** | **0** | **8** | **2** | **1** | **0** |
| **Rippling** | **9** | **1** | **0** | **0** | **9** | **1** | **1** | **0** |
| **Sage** | **10** | **0** | **0** | **0** | **9** | **1** | **1** | **0** |
| **SAP** | **8** | **2** | **0** | **0** | **8** | **2** | **1** | **0** |
| **Stackone** | **9** | **1** | **0** | **0** | **9** | **1** | **1** | **0** |
| **Workday** | **8** | **0** | **0** | **2** | **9** | **1** | **1** | **0** |

### Gesamtwerte Complete Architecture:
- **Original**: Precision 94.5%, Recall 100.0%, F1-Score 97.1%
- **Korrigiert**: Precision **87.2%**, Recall **84.5%**, F1-Score **85.9%**
- **Differenz**: -7.3% Precision, -15.5% Recall, -11.2% F1-Score

**Problem**: Die ursprünglichen Werte behaupteten einen **perfekten Recall von 100%** (0 False Negatives), was **nicht stimmt**. Tatsächlich gab es 15 False Negatives.

**Kritischer Fehler**: ADB hatte massive Abweichungen (3 TP statt 10, 7 FN statt 0).

---

## 5. Zusammenfassung aller Methoden (Tabelle 5)

### Original vs. Korrigiert:

| Methode | Original P% | Original R% | Original F1% | Korrigiert P% | Korrigiert R% | Korrigiert F1% | Differenz F1 |
|---------|-------------|-------------|--------------|---------------|---------------|----------------|--------------|
| Single-Prompt | 97.5 | 73.8 | **84.0** | 89.2 | 68.0 | **77.2** | **-6.8%** |
| Basic RAG | 85.4 | 92.6 | **88.9** | 88.2 | 90.7 | **89.4** | **+0.5%** |
| Enhanced RAG | 93.2 | 98.0 | **95.5** | 79.8 | 77.6 | **78.7** | **-16.8%** |
| Complete Arch | 94.4 | 100.0 | **97.1** | 87.2 | 84.5 | **85.9** | **-11.2%** |

### Gesamtzähler:

| Methode | Orig. TP | Orig. FP | Orig. FN | Orig. TN | Korr. TP | Korr. FP | Korr. FN | Korr. TN |
|---------|----------|----------|----------|----------|----------|----------|----------|----------|
| Single-Prompt | **79** | **2** | **28** | **1** | **66** | **8** | **31** | **5** |
| Basic RAG | **88** | **15** | **7** | **0** | **97** | **13** | **10** | **1** |
| Enhanced RAG | **96** | **7** | **2** | **5** | **83** | **21** | **24** | **3** |
| Complete Arch | **102** | **6** | **0** | **2** | **82** | **12** | **15** | **1** |

---

## Hauptfehlerquellen

### 1. **Fehlende oder falsche Ground Truth Vergleiche**
Die ursprünglichen Tabellen basierten wahrscheinlich nicht auf systematischen Vergleichen zwischen Mapping-Ergebnissen und Ground Truth-Dateien.

### 2. **Überschätzung der Enhanced RAG Performance**
Die Enhanced RAG Methode zeigte die größten Abweichungen (-16.8% F1-Score). Die ursprünglichen Werte suggerierten eine nahezu perfekte Performance, die nicht den Fakten entspricht.

### 3. **Falsche Annahme von "Null False Negatives" bei Complete Architecture**
Die Behauptung, dass die Complete Architecture **keine False Negatives** hat (100% Recall), war falsch. Tatsächlich gab es 15 FN.

### 4. **Fehlende ADB-Daten in Single-Prompt**
In der Single-Prompt-Methode fehlte die `adp_mapping.json` Datei im `singel_prompt` Ordner, was zu 0/0/0/0 führte.

### 5. **Inkonsistente Flip-Daten in Enhanced RAG**
Die Flip-Mapping-Datei in Enhanced RAG hatte ein komplett falsches Format oder falsche Mappings, was zu 0 TP führte.

---

## Empfehlungen

1. **Automatische Verifizierung**: Das erstellte Python-Script (`verify_results.py`) sollte bei jeder Datenaktualisierung ausgeführt werden.

2. **Ground Truth Pflege**: Sicherstellen, dass alle Ground Truth-Dateien vollständig und korrekt sind.

3. **Dateistruktur-Konsistenz**: Alle Mapping-Dateien sollten dasselbe JSON-Format verwenden (dict vs. list für "mapped_fields").

4. **Dokumentation der Metriken**: Klare Definition, wie TP, FP, FN, TN berechnet werden.

5. **Peer Review**: Ergebnisse sollten von mindestens einer weiteren Person geprüft werden.

---

## Fazit

Die **korrigierten Ergebnisse** zeigen ein **realistischeres Bild** der Performance:

- **Single-Prompt** ist **schwächer** als ursprünglich angegeben (77.2% statt 84.0% F1)
- **Basic RAG** ist **nahezu korrekt** (89.4% statt 88.9% F1)
- **Enhanced RAG** ist **deutlich schwächer** als behauptet (78.7% statt 95.5% F1)
- **Complete Architecture** ist **stark**, aber **nicht perfekt** (85.9% statt 97.1% F1)

Die **größte Verbesserung** zeigt sich tatsächlich zwischen Single-Prompt und Basic RAG (+12.2% F1), nicht wie ursprünglich behauptet zwischen Enhanced RAG und Complete Architecture.

