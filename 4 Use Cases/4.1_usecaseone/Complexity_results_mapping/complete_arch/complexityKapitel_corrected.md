Die Komplexitätsanalyse der Mappings auf Basis der Complete Architecture zeigt eine ausgewogene Fehlerverteilung über die drei Komplexitätstypen: 4 Direct-Fehler, 5 Conversion-Fehler und 5 Logical-Fehler. Von insgesamt 100 möglichen Feld-Zuordnungen (10 APIs × 10 Felder) wurden 86 korrekt gemappt, was einer Gesamtgenauigkeit von 86,0% entspricht.

Feldspezifisch zeigen sich die meisten Ausfälle bei `status` (4 Fehler: ADP/Conversion, Oracle/Direct, Personio/Conversion, SAP/Logical) und `unit` (4 Fehler: HiBob/Logical, Oracle/Logical, Personio/Logical, Sage/Direct), gefolgt von `amount` (2 Fehler: ADP/Conversion, Personio/Logical) sowie jeweils einzelnen Fehlern bei `employee_note` (ADP/Conversion), `end_date` (Workday/Conversion), `start_half_day` (Workday/Direct) und `end_half_day` (Workday/Direct). Die Felder `employee_external_id`, `absence_type_external_id` und `start_date` wurden über alle APIs hinweg fehlerfrei gemappt.

Im Systemvergleich nach Komplexitätsgraden ergibt sich folgendes Bild:

• **Direct** (4 Fehler): Schwachstellen bei Oracle (`status`), Sage (`unit`) und Workday (`start_half_day`, `end_half_day`); fehlerfreie Handhabung bei ADP, BambooHR, HiBob, Personio, Rippling, SAP und StackOne.

• **Conversion** (5 Fehler): Ausfälle bei ADP (`status`, `amount`, `employee_note`), Personio (`status`) und Workday (`end_date`); stabile Performance bei BambooHR, HiBob, Oracle, Rippling, Sage, SAP und StackOne.

• **Logical** (5 Fehler): Probleme bei HiBob (`unit`), Oracle (`unit`), Personio (`amount`, `unit`) und SAP (`status`); robuste Ergebnisse bei ADP, BambooHR, Rippling, Sage, StackOne und Workday.

Die Analyse offenbart systemspezifische Herausforderungen: Workday zeigt mit 4 Fehlern die meisten Mapping-Probleme, primär aufgrund fehlender Half-Day-Unterstützung in der API. ADP und Personio weisen jeweils 3 Fehler auf, konzentriert auf Status- und Berechnungsfelder. Die Fehlerverteilung zeigt, dass Direct-Mappings trotz ihrer konzeptionellen Einfachheit nicht fehlerunanfällig sind, während Conversion- und Logical-Mappings erwartungsgemäß höhere Fehlerraten aufweisen. Die perfekte Abdeckung der Basisfelder (Mitarbeiter-ID, Abwesenheitstyp, Startdatum) demonstriert die Stärke der Architektur bei fundamentalen Mappings, während komplexe Status- und Berechnungslogiken die Hauptfehlerquellen darstellen.

