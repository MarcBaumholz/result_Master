# Evaluationsergebnisse der API-Mapping-Ansätze

## Metriken-Definition

Die Evaluation basiert auf klassischen Konfusionsmatrix-Metriken:

* **True Positives (TP)**: Das System erkennt korrekte Feldzuordnungen korrekt
* **True Negatives (TN)**: Das System lehnt falsche oder nicht vorhandene Zuordnungen korrekt ab
* **False Positives (FP)**: Das System erfindet Zuordnungen, die nicht existieren (Halluzinationen)
* **False Negatives (FN)**: Das System übersieht gültige Zuordnungen und gibt an, dass diese nicht existieren

### Matching-Kriterium (Relaxed)
Ein Mapping wird als korrekt gewertet, wenn das Ground-Truth-Feld im gemappten Feld enthalten ist.
Beispiel: Ground Truth `leaveTypeCode.codeValue` matched mit `data.transform.workerLeave.leaveAbsence.leaveTypeCode.codeValue`

---

## 1. Single-Prompt Ansatz

Die Single-Prompt-Variante arbeitet ausschließlich auf Basis des intrinsischen Trainingswissens des Sprachmodells ohne externe Kontextanreicherung.

### Tabelle 1: Single-Prompt Ergebnisse

| API Spec Name | TP | FP | FN | TN | Precision (%) | Recall (%) | F1-Score (%) |
|---------------|----|----|----|----|---------------|------------|--------------|
| Flip          | 9  | 1  | 1  | 0  | 90.0          | 90.0       | 90.0         |
| ADP           | 3  | 1  | 4  | 3  | 75.0          | 42.9       | 54.5         |
| BambooHR      | 7  | 0  | 3  | 0  | 100.0         | 70.0       | 82.4         |
| HiBob         | 7  | 1  | 2  | 1  | 87.5          | 77.8       | 82.4         |
| Oracle        | 7  | 1  | 1  | 2  | 87.5          | 87.5       | 87.5         |
| Personio      | 6  | 1  | 1  | 3  | 85.7          | 85.7       | 85.7         |
| Rippling      | 4  | 6  | 1  | 0  | 40.0          | 80.0       | 53.3         |
| Sage          | 3  | 5  | 2  | 1  | 37.5          | 60.0       | 46.2         |
| SAP           | 0  | 1  | 8  | 2  | 0.0           | 0.0        | 0.0          |
| StackOne      | 6  | 4  | 1  | 0  | 60.0          | 85.7       | 70.6         |
| Workday       | 4  | 1  | 3  | 3  | 80.0          | 57.1       | 66.7         |

**Gesamt**: Precision=**71.8%**, Recall=**67.5%**, F1=**69.6%** (TP=56, FP=22, FN=27, TN=15)

### Analyse Single-Prompt

Die Single-Prompt-Methode zeigt die **beste Gesamtperformance** aller vier Ansätze mit einem ausgeglichenen F1-Score von 69.6%. Besonders hervorzuheben:

**Stärken:**
- ✅ **Beste Precision** (71.8%) - Niedrigste Halluzinationsrate
- ✅ Exzellente Ergebnisse bei einfachen APIs: Flip (90%), BambooHR (82.4%)
- ✅ Sehr gute Performance bei strukturierten APIs: Oracle (87.5%), Personio (85.7%)
- ✅ Niedrige False-Positive-Rate (22) zeigt geringe Neigung zu Halluzinationen

**Schwächen:**
- ❌ **SAP komplett gescheitert** (0% F1-Score) - Zu komplex für reines LLM-Wissen
- ⚠️ Schwache Performance bei Enterprise-APIs: Sage (46.2%), Rippling (53.3%)
- ⚠️ Moderate False-Negative-Rate (27) - Viele korrekte Mappings werden übersehen

**Schlussfolgerung:**
Single-Prompt eignet sich hervorragend für standardisierte APIs mit klarer Dokumentation, versagt jedoch bei hochkomplexen Enterprise-Systemen wie SAP.

---

## 2. Basic RAG Ansatz

Die Integration eines grundlegenden Retrieval-Augmented-Generation-Ansatzes erweitert die Single-Prompt-Baseline um direkten Zugriff auf externe Wissenquellen.

### Tabelle 2: Basic RAG Ergebnisse

| API Spec Name | TP | FP | FN | TN | Precision (%) | Recall (%) | F1-Score (%) |
|---------------|----|----|----|----|---------------|------------|--------------|
| Flip          | 9  | 1  | 1  | 0  | 90.0          | 90.0       | 90.0         |
| ADP           | 1  | 9  | 1  | 0  | 10.0          | 50.0       | 16.7         |
| BambooHR      | 4  | 6  | 0  | 0  | 40.0          | 100.0      | 57.1         |
| HiBob         | 1  | 9  | 1  | 0  | 10.0          | 50.0       | 16.7         |
| Oracle        | 0  | 10 | 1  | 0  | 0.0           | 0.0        | 0.0          |
| Personio      | 2  | 8  | 1  | 0  | 20.0          | 66.7       | 30.8         |
| Rippling      | 3  | 7  | 1  | 0  | 30.0          | 75.0       | 42.9         |
| Sage          | 1  | 9  | 1  | 0  | 10.0          | 50.0       | 16.7         |
| SAP           | 0  | 10 | 1  | 0  | 0.0           | 0.0        | 0.0          |
| StackOne      | 5  | 5  | 1  | 0  | 50.0          | 83.3       | 62.5         |
| Workday       | 3  | 7  | 1  | 0  | 30.0          | 75.0       | 42.9         |

**Gesamt**: Precision=**26.4%**, Recall=**74.4%**, F1=**38.9%** (TP=29, FP=81, FN=10, TN=0)

### Analyse Basic RAG

Basic RAG zeigt ein **extremes Ungleichgewicht**: Höchster Recall (74.4%), aber **drastisch niedrige Precision** (26.4%).

**Stärken:**
- ✅ **Höchster Recall** (74.4%) - Findet die meisten korrekten Mappings
- ✅ Niedrigste False-Negative-Rate (10) - Übersieht kaum korrekte Zuordnungen
- ✅ Gute Performance bei BambooHR (100% Recall), StackOne (83.3% Recall)

**Kritische Schwächen:**
- ❌ **Massive Halluzinationsproblematik** - 81 False Positives!
- ❌ **Katastrophale Precision** (26.4%) - 3 von 4 Mappings sind falsch
- ❌ Oracle & SAP: Komplett gescheitert (0% F1)
- ❌ ADP & HiBob: Nur 10% Precision - praktisch unbrauchbar
- ❌ **Keine True Negatives** - System erkennt unmappbare Felder nicht

**Schlussfolgerung:**
Basic RAG ist **nicht produktionsreif**. Der Ansatz retrieft zwar relevante Informationen, interpretiert diese aber unkontrolliert und generiert massiv falsche Mappings. Das System "rät" eher, als dass es präzise mappt.

---

## 3. Enhanced RAG Ansatz

Die erweiterte RAG-Konfiguration mit strukturierten Retrieval-Pipelines und intelligenter Terminologie-Normalisierung zielt darauf ab, den Retrieval-Prozess zu optimieren.

### Tabelle 3: Enhanced RAG Ergebnisse

| API Spec Name | TP | FP | FN | TN | Precision (%) | Recall (%) | F1-Score (%) |
|---------------|----|----|----|----|---------------|------------|--------------|
| Flip          | 0  | 10 | 10 | 0  | 0.0           | 0.0        | 0.0          |
| ADP           | 6  | 4  | 1  | 0  | 60.0          | 85.7       | 70.6         |
| BambooHR      | 6  | 4  | 0  | 0  | 60.0          | 100.0      | 75.0         |
| HiBob         | 1  | 9  | 1  | 0  | 10.0          | 50.0       | 16.7         |
| Oracle        | 0  | 10 | 1  | 0  | 0.0           | 0.0        | 0.0          |
| Personio      | 6  | 1  | 1  | 2  | 85.7          | 85.7       | 85.7         |
| Rippling      | 8  | 2  | 1  | 0  | 80.0          | 88.9       | 84.2         |
| Sage          | 1  | 9  | 1  | 0  | 10.0          | 50.0       | 16.7         |
| SAP           | 2  | 8  | 1  | 0  | 20.0          | 66.7       | 30.8         |
| StackOne      | 7  | 3  | 1  | 0  | 70.0          | 87.5       | 77.8         |
| Workday       | 3  | 4  | 2  | 2  | 42.9          | 60.0       | 50.0         |

**Gesamt**: Precision=**38.5%**, Recall=**66.7%**, F1=**48.8%** (TP=40, FP=64, FN=20, TN=4)

### Analyse Enhanced RAG

Enhanced RAG verbessert die Precision gegenüber Basic RAG um 12%, bleibt aber **weit hinter Single-Prompt** zurück.

**Stärken:**
- ✅ **Top-Performance bei Rippling** (84.2% F1) und StackOne (77.8% F1)
- ✅ Exzellente Personio-Ergebnisse (85.7% F1) - Sogar besser als Single-Prompt
- ✅ Deutlich weniger False Positives als Basic RAG (64 vs. 81)
- ✅ Guter Recall bei ADP (85.7%) und BambooHR (100%)

**Massive Schwächen:**
- ❌ **Flip komplett gescheitert** (0% F1) - Paradox: Referenz-API versagt!
- ❌ Oracle vollständig fehlgeschlagen (0% F1)
- ❌ Immer noch hohe Halluzinationsrate (64 FP)
- ❌ HiBob & Sage bleiben katastrophal (10% Precision)
- ⚠️ Inkonsistente Performance - Große Schwankungen zwischen APIs

**Schlussfolgerung:**
Enhanced RAG zeigt **extreme Inkonsistenz**. Während einige APIs (Rippling, Personio) hervorragend funktionieren, versagt das System bei anderen komplett (Flip, Oracle). Die Verbesserungen sind zu instabil für Produktiveinsatz.

---

## 4. Complete Architecture Ansatz

Die vollständige Architektur mit integriertem Tool-Use, Validierungs- und Verifikationsmodulen repräsentiert das final entwickelte System.

### Tabelle 4: Complete Architecture Ergebnisse

| API Spec Name | TP | FP | FN | TN | Precision (%) | Recall (%) | F1-Score (%) |
|---------------|----|----|----|----|---------------|------------|--------------|
| Flip          | 0  | 0  | 10 | 0  | 0.0           | 0.0        | 0.0          |
| ADP           | 3  | 1  | 4  | 3  | 75.0          | 42.9       | 54.5         |
| BambooHR      | 4  | 6  | 0  | 0  | 40.0          | 100.0      | 57.1         |
| HiBob         | 1  | 9  | 1  | 0  | 10.0          | 50.0       | 16.7         |
| Oracle        | 7  | 3  | 1  | 0  | 70.0          | 87.5       | 77.8         |
| Personio      | 6  | 4  | 1  | 0  | 60.0          | 85.7       | 70.6         |
| Rippling      | 8  | 2  | 1  | 0  | 80.0          | 88.9       | 84.2         |
| Sage          | 1  | 9  | 1  | 0  | 10.0          | 50.0       | 16.7         |
| SAP           | 4  | 6  | 1  | 0  | 40.0          | 80.0       | 53.3         |
| StackOne      | 7  | 3  | 1  | 0  | 70.0          | 87.5       | 77.8         |
| Workday       | 3  | 7  | 1  | 0  | 30.0          | 75.0       | 42.9         |

**Gesamt**: Precision=**46.8%**, Recall=**66.7%**, F1=**55.0%** (TP=44, FP=50, FN=22, TN=3)

### Analyse Complete Architecture

Complete Architecture verbessert die Precision gegenüber beiden RAG-Ansätzen, erreicht aber **nicht die Single-Prompt Performance**.

**Stärken:**
- ✅ **Beste Rippling-Performance** (84.2% F1) - Gleichauf mit Enhanced RAG
- ✅ Starke Oracle-Ergebnisse (77.8% F1) - Deutlich besser als andere Ansätze
- ✅ Deutlich weniger False Positives als RAG-Ansätze (50 vs. 64/81)
- ✅ Guter Recall (66.7%) mit moderater Precision (46.8%)
- ✅ Verbesserte SAP-Performance (53.3% F1) gegenüber Single-Prompt (0%)

**Schwächen:**
- ❌ **Flip komplett ausgefallen** (0% F1) - Kritischer Fehler
- ❌ Immer noch hohe Halluzinationsrate (50 FP)
- ❌ HiBob & Sage weiterhin katastrophal (10% Precision)
- ⚠️ Erreicht nicht die Stabilität von Single-Prompt
- ⚠️ Workday verschlechtert gegenüber Single-Prompt (42.9% vs. 66.7%)

**Schlussfolgerung:**
Complete Architecture zeigt **Potenzial bei komplexen APIs** (Oracle, SAP), kann aber die Konsistenz von Single-Prompt nicht erreichen. Die Tool-Integration hilft bei schwierigen Cases, führt aber zu Instabilität bei einfacheren APIs.

---

## 5. Gesamtvergleich und Zusammenfassung

### Tabelle 5: Ergebnisse aller Methoden

| Methode                 | Precision (%) | Recall (%) | F1-Score (%) | Gesamt TP | Gesamt FP | Gesamt FN | Gesamt TN |
|-------------------------|---------------|------------|--------------|-----------|-----------|-----------|-----------|
| Single-Prompt           | **71.8**      | 67.5       | **69.6**     | 56        | **22**    | 27        | **15**    |
| Basic RAG               | 26.4          | **74.4**   | 38.9         | 29        | 81        | **10**    | 0         |
| Enhanced RAG            | 38.5          | 66.7       | 48.8         | 40        | 64        | 20        | 4         |
| Complete Architecture   | 46.8          | 66.7       | 55.0         | 44        | 50        | 22        | 3         |

### Kritische Erkenntnisse

#### 1. **Single-Prompt ist der klare Gewinner** 🏆
- Beste Balance zwischen Precision und Recall
- Niedrigste Halluzinationsrate (22 FP)
- Konsistente Performance über verschiedene APIs
- **Empfehlung**: Produktiveinsatz für standardisierte APIs

#### 2. **Basic RAG ist unbrauchbar** ❌
- Katastrophale Precision (26.4%)
- Massive Halluzinationsproblematik (81 FP)
- 3 von 4 Mappings sind falsch
- **Empfehlung**: Nicht einsetzen ohne fundamentale Überarbeitung

#### 3. **RAG-Ansätze zeigen hohe Varianz** ⚠️
- Enhanced RAG: Flip 0% vs. Personio 85.7%
- Complete Arch: Flip 0% vs. Rippling 84.2%
- Unpredictable Performance
- **Empfehlung**: Nur für spezifische APIs nach gründlichem Testing

#### 4. **Komplexität korreliert nicht mit Performance** 🤔
- SAP (sehr komplex): Alle Ansätze schwach
- Flip (Referenz-API): Enhanced RAG & Complete Arch versagen komplett
- Oracle (komplex): Complete Arch am besten (77.8%)
- **Erkenntnis**: API-Struktur wichtiger als Komplexität

#### 5. **Die "problematischen Fünf"** 🚨
Diese APIs zeigen durchgehend schlechte Ergebnisse:
- **Sage**: Bester F1 nur 46.2% (Single-Prompt)
- **SAP**: Bester F1 nur 53.3% (Complete Arch)
- **HiBob**: Bester F1 nur 82.4% (Single-Prompt)
- **Workday**: Bester F1 nur 66.7% (Single-Prompt)
- **Flip** (bei RAG): 0% bei Enhanced RAG & Complete Arch

### API-spezifische Empfehlungen

| API       | Bester Ansatz          | F1-Score | Begründung                                    |
|-----------|------------------------|----------|-----------------------------------------------|
| Flip      | Single-Prompt / Basic RAG | 90.0%    | RAG-Ansätze versagen komplett                |
| ADP       | Enhanced RAG           | 70.6%    | Einziger Ansatz mit >60% F1                   |
| BambooHR  | Single-Prompt          | 82.4%    | Beste Balance, 100% Precision                 |
| HiBob     | Single-Prompt          | 82.4%    | Alle anderen Ansätze katastrophal             |
| Oracle    | Single-Prompt          | 87.5%    | Konsistent gut (Complete Arch auch ok)        |
| Personio  | Single-Prompt / Enhanced RAG | 85.7%    | Beide gleichauf                              |
| Rippling  | Enhanced RAG / Complete Arch | 84.2%    | RAG-Ansätze deutlich überlegen               |
| Sage      | Single-Prompt          | 46.2%    | Alle Ansätze schwach, SP am wenigsten schlecht |
| SAP       | Complete Architecture  | 53.3%    | Einziger Ansatz mit >0%                       |
| StackOne  | Single-Prompt          | 70.6%    | Beste Balance trotz hoher Komplexität         |
| Workday   | Single-Prompt          | 66.7%    | RAG-Ansätze deutlich schlechter               |

### Handlungsempfehlungen

#### Sofort umsetzbar:
1. ✅ **Single-Prompt als Standard-Ansatz** für 8 von 11 APIs verwenden
2. ❌ **Basic RAG komplett deaktivieren** - Zu gefährlich in Production
3. ⚠️ **Enhanced RAG nur für Rippling & ADP** einsetzen
4. 🔧 **Complete Arch nur für SAP & Oracle** verwenden

#### Mittelfristig erforderlich:
1. 🔍 **Root-Cause-Analyse** für Flip-Versagen bei RAG-Ansätzen
2. 🛠️ **Spezial-Handler** für Sage, SAP, Workday entwickeln
3. 📊 **Halluzinations-Filter** für RAG-Ansätze implementieren
4. ✅ **Hybrid-Ansatz** entwickeln: Single-Prompt + selektives RAG

#### Langfristig strategisch:
1. 🎯 **API-spezifische Optimierung** statt One-Size-Fits-All
2. 🤖 **Automatische Ansatz-Selektion** basierend auf API-Charakteristika
3. 🔬 **Ground-Truth-Verifizierung** für schwache APIs
4. 📈 **Kontinuierliches Monitoring** der Production-Performance

---

## Fazit

Die Evaluation zeigt ein **überraschendes Ergebnis**: Der einfachste Ansatz (Single-Prompt) liefert die besten Gesamtergebnisse. Die komplexeren RAG-Ansätze verbessern zwar den Recall, führen aber zu **massiven Halluzinationsproblemen** und **instabiler Performance**.

**Zentrale Erkenntnis**: Mehr Komplexität führt nicht automatisch zu besseren Ergebnissen. Die Kunst liegt darin, **den richtigen Ansatz für die richtige API** zu wählen.

Für einen **produktionsreifen Einsatz** empfiehlt sich ein **intelligenter Hybrid-Ansatz**:
- Single-Prompt als stabiles Fundament
- Selektiver RAG-Einsatz nur bei nachgewiesener Überlegenheit
- API-spezifische Fallback-Strategien
- Kontinuierliche Halluzinations-Überwachung

**Die nächsten Schritte**: Fokus auf die "problematischen Fünf" APIs und Entwicklung spezialisierter Mapping-Strategien für Sage, SAP, HiBob, Workday und die Behebung des Flip-Problems bei RAG-Ansätzen.

