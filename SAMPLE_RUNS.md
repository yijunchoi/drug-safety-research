# Sample runs

Generated 2026-11-12 against http://127.0.0.1:8000 by `uv run sample_runs.py http://127.0.0.1:8000`.


## 1. Since 2020, have FDA reports of pancreatitis for semaglutide (Ozempic, Wegovy) grown faster than the number of Medicare patients taking it, and does its official FDA label warn about pancreatitis?

### Expected (computed directly from openFDA, no model)

US reports listing PANCREATITIS, by year received: 2020: 143 US reports / 297,488 Medicare users = 48.1 per 100k; 2021: 126 US reports / 566,867 Medicare users = 22.2 per 100k; 2022: 120 US reports / 964,868 Medicare users = 12.4 per 100k; 2023: 150 US reports / 1,750,208 Medicare users = 8.6 per 100k; 2024: 225 US reports / 2,315,591 Medicare users = 9.7 per 100k. Pancreatitis on the current label: yes.

Source: `/drug/event.json` count by receivedate (https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate), `data/medicare_part_d_users.csv` (CMS Medicare Part D Spending by Drug) and `/drug/label.json` (https://api.fda.gov/drug/label.json?search=openfda.generic_name%3A%22semaglutide%22&limit=20)

### This agent

**Short answer:** No, US reports of pancreatitis for semaglutide have not grown faster than the number of Medicare patients taking the drug, as the number of reports per 100,000 users has decreased since 2020 ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)) ([CMS](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug)). Yes, the drug's official FDA label—which is the official prescribing information that comes with the drug and lists its known risks—warns patients and doctors about the potential for pancreatitis ([DailyMed](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)).

### Pancreatitis Reports vs. Medicare Patients

While the total number of yearly US reports of pancreatitis has fluctuated, the number of Medicare Part D patients prescribed semaglutide has grown significantly ([CMS](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug)). Because of this rapid increase in use, the number of US pancreatitis reports per 100,000 Medicare users dropped from 48.1 in 2020 down to 9.7 in 2024 ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)) ([CMS](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug)).

The table below compares the US reports of pancreatitis to Medicare Part D users and shows the number of reports per 100,000 users, utilizing data from the FDA Adverse Event Reporting System ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22PANCREATITIS%22+AND+occurcountry%3A%22US%22+AND+receivedate%3A%5B20200101+TO+20241231%5D&count=receivedate)) and Medicare user records ([CMS](https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug)).

| Year | Medicare Part D Users | US Pancreatitis Reports | Reports per 100,000 Users |
| :--- | :--- | :--- | :--- |
| 2020 | 297,488 | 143 | 48.1 |
| 2021 | 566,867 | 126 | 22.2 |
| 2022 | 964,868 | 120 | 12.4 |
| 2023 | 1,750,208 | 150 | 8.6 |
| 2024 | 2,315,591 | 225 | 9.7 |

### FDA Label Warnings

The official FDA label for semaglutide (brand Ozempic) explicitly warns about acute pancreatitis ([DailyMed](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)). 

* **Warnings and Precautions (Section 5.2):** States that acute pancreatitis has been observed in patients treated with GLP-1 receptor agonists, including Ozempic, and instructs healthcare providers to discontinue the drug if pancreatitis is suspected ([DailyMed](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)).
* **Adverse Reactions:** Lists acute pancreatitis as a serious adverse reaction ([DailyMed](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)).
* **Patient Guidance:** Both the Medication Guide and Patient Information sections warn patients about the potential risk of pancreas inflammation and instruct them to immediately stop taking the medication and call their doctor if they experience severe pain in their stomach area ([DailyMed](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=42bdd912-2393-44c4-b7e0-47672ca28991)).

### What this data can't tell you

* **Side-effect reports:** These reports do not prove that semaglutide caused the pancreatitis. The FDA Adverse Event Reporting System (FAERS) does not track the total number of people taking the drug worldwide, meaning it cannot provide a true risk rate. Additionally, side-effect reporting frequently increases when a drug receives significant news coverage.
* **Medicare rates:** The calculated reporting rate is only a rough index specifically for Medicare patients, who are typically older or have specific disabilities, and may not represent the reporting rate for all people taking the drug.
* **Unanswered questions:** The findings did not include Medicare user counts or US-specific report rates for 2025 or 2026, so we cannot calculate the exact report rates for those years. No recall data was analyzed for this report.

_Not medical advice: talk to your doctor or pharmacist._

<details><summary>Trace: 9 tool calls, 4 researchers</summary>

| Agent | Tool | Arguments |
| --- | --- | --- |
| Lead | `resolve_drug_name` | `{"name": "semaglutide"}` |
| Lead | `research` | `{"task": "Get yearly FAERS reports of pancreatitis for semaglutide from 2020 to present"}` |
| Lead | `research` | `{"task": "Get Medicare Part D patient counts for semaglutide by year from 2020 to present"}` |
| Lead | `research` | `{"task": "Determine if the FDA label for semaglutide warns about pancreatitis"}` |
| Lead | `research` | `{"task": "Calculate FAERS pancreatitis reports per 100,000 Medicare Part D users for semaglutide by year since 2020 (use` |
| Researcher 1 | `faers_trend` | `{"reaction": "PANCREATITIS", "drug": "semaglutide"}` |
| Researcher 2 | `medicare_users` | `{"drug": "semaglutide"}` |
| Researcher 3 | `label_warnings` | `{"find": "pancreatitis", "drug": "semaglutide"}` |
| Researcher 4 | `faers_report_rate` | `{"drug": "semaglutide", "reaction": "PANCREATITIS"}` |

Full results: `tool_calls` in the /chat response.
</details>

### Same model, no tools and no system prompt

To answer your questions accurately, we can look at the data surrounding the rise of semaglutide (Ozempic and Wegovy), the patterns in FDA adverse event reporting, and the official FDA prescribing information.

---

### Part 1: Have FDA reports of pancreatitis grown faster than Medicare patients taking semaglutide?

While both the number of pancreatitis reports in the FDA Adverse Event Reporting System (FAERS) and the number of Medicare patients taking semaglutide have surged dramatically since 2020, **there is no evidence showing that pancreatitis reports have grown *faster* than the rate of patient uptake.** 

Instead, the rise in pancreatitis reports appears to scale with—or lag behind—the massive, exponential growth of prescriptions. 

Here is how the data breaks down:

#### 1. The Growth of Medicare Patients Taking Semaglutide
According to data analyzed by the Kaiser Family Foundation (KFF) and researchers tracking Medicare Part D claims, utilization of semaglutide has grown exponentially since 2020:
* **Ozempic (for Type 2 Diabetes):** In 2020, there were roughly **240,000** Medicare Part D beneficiaries prescribed Ozempic. By 2023, that number had surged to well **over 1 million** beneficiaries—a several-fold (more than 400%) increase.
* **Wegovy (for Weight Loss / CV Risk):** Wegovy was approved in mid-2021. Because Medicare is legally barred from covering weight-loss drugs, utilization was initially very low. However, in early 2024, Medicare allowed coverage for Wegovy for the prevention of major cardiovascular events, leading to a new wave of Medicare utilization.

#### 2. The Rise in FDA Adverse Event Reports (FAERS)
As expected with any block-buster drug, FAERS reports of pancreatitis associated with semaglutide have increased significantly since 2020. However, researchers point out two critical factors:
* **The "Denominator" Effect:** When millions of new patients start taking a drug, the absolute number of side-effect reports will naturally rise, even if the actual risk (the percentage rate of patients getting pancreatitis) remains flat or very low. 
* **Stimulated Reporting:** Media attention surrounding "Ozempic side effects" since late 2022 has prompted a surge in voluntary reporting by patients and doctors, known as stimulated reporting. 

Epidemiological studies comparing GLP-1 receptor agonists (like semaglutide) to other diabetes medications show that while there is a slightly elevated risk of acute pancreatitis associated with GLP-1s (estimated at roughly 1 to 2 cases per 1,000 patient-years), the rate has not spiked disproportionately to the millions of new users. 

*Note: The FDA emphasizes that FAERS data consists of voluntary, unverified reports and cannot be used alone to calculate the exact incidence rate of a side effect.*

---

### Part 2: Does the official FDA label warn about pancreatitis?

**Yes.** The official FDA-approved prescribing information (the label) for both **Ozempic** and **Wegovy** contains explicit warnings about pancreatitis. 

Under **Section 5 (Warnings and Precautions)**, the labels state:

* **Acute Pancreatitis:** Acute pancreatitis, including fatal and non-fatal hemorrhagic or necrotizing pancreatitis, has been observed in patients treated with GLP-1 receptor agonists in clinical trials and post-marketing.
* **Instructions to Providers/Patients:** 
  * Patients should be observed carefully for signs and symptoms of pancreatitis (including persistent, severe abdominal pain, sometimes radiating to the back, which may or may not be accompanied by vomiting).
  * If pancreatitis is suspected, semaglutide should be discontinued promptly and appropriate management initiated.
  * If pancreatitis is confirmed, semaglutide should not be restarted.

Because pancreatitis is a known potential risk of all GLP-1 receptor agonists, it has been included on the warning labels of these drugs since their initial FDA approvals (2017 for Ozempic, 2021 for Wegovy).


## 2. Compare semaglutide, tirzepatide and liraglutide: what share of each drug's FDA adverse event reports mention suicidal ideation?

### Expected (computed directly from openFDA, no model)

semaglutide: 520 of 78023 reports (0.67%); tirzepatide: 509 of 181068 reports (0.28%); liraglutide: 169 of 51303 reports (0.33%).

Source: `/drug/event.json` report totals, with and without `patient.reaction.reactionmeddrapt:"SUICIDAL IDEATION"`

### This agent

**Short answer:** Based on reports submitted to the FDA, semaglutide reports mention suicidal ideation in 0.7% of the total, while tirzepatide and liraglutide reports mention it in 0.3% of their respective totals ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1), [openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22tirzepatide%22+OR+patient.drug.openfda.brand_name%3A%22tirzepatide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1), [openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22liraglutide%22+OR+patient.drug.openfda.brand_name%3A%22liraglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)). This means that out of all submitted adverse event reports, only a small share for each drug mentions this issue ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1), [openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22tirzepatide%22+OR+patient.drug.openfda.brand_name%3A%22tirzepatide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1), [openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22liraglutide%22+OR+patient.drug.openfda.brand_name%3A%22liraglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)).

### Comparing Semaglutide, Tirzepatide, and Liraglutide

The following table compares the total reports and the share mentioning suicidal ideation for each drug based on openFDA FAERS database search results ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1), [openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22tirzepatide%22+OR+patient.drug.openfda.brand_name%3A%22tirzepatide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1), [openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22liraglutide%22+OR+patient.drug.openfda.brand_name%3A%22liraglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)).

| Drug | Total Reports | Reports Mentioning Suicidal Ideation | Share of Reports |
| :--- | :--- | :--- | :--- |
| Semaglutide | 78,023 | 520 | 0.7% |
| Tirzepatide | 181,068 | 509 | 0.3% |
| Liraglutide | 51,303 | 169 | 0.3% |

#### Semaglutide
Out of 78,023 total FAERS reports submitted for semaglutide, 520 reports (0.7%) mention suicidal ideation ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22semaglutide%22+OR+patient.drug.openfda.brand_name%3A%22semaglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)).

#### Tirzepatide
Out of 181,068 total FAERS reports submitted for tirzepatide, 509 reports (0.3%) mention suicidal ideation ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22tirzepatide%22+OR+patient.drug.openfda.brand_name%3A%22tirzepatide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)).

#### Liraglutide
Out of 51,303 total FAERS reports submitted for liraglutide, 169 reports (0.3%) mention suicidal ideation ([openFDA FAERS](https://api.fda.gov/drug/event.json?search=%28patient.drug.openfda.generic_name%3A%22liraglutide%22+OR+patient.drug.openfda.brand_name%3A%22liraglutide%22%29+AND+patient.reaction.reactionmeddrapt%3A%22SUICIDAL+IDEATION%22&limit=1)).

### What this data can't tell you

The side-effect reports in FAERS do not prove that the drug caused the reported problem. FAERS does not track the total number of people successfully taking these drugs, meaning there is no way to calculate an actual rate of occurrence. Additionally, public reporting often rises when a drug receives intense news and media coverage. 

_Not medical advice: talk to your doctor or pharmacist._

<details><summary>Trace: 6 tool calls, 1 researchers</summary>

| Agent | Tool | Arguments |
| --- | --- | --- |
| Lead | `resolve_drug_name` | `{"name": "semaglutide"}` |
| Lead | `resolve_drug_name` | `{"name": "tirzepatide"}` |
| Lead | `resolve_drug_name` | `{"name": "liraglutide"}` |
| Lead | `research` | `{"task": "Compare the share of FAERS adverse event reports that mention suicidal ideation for semaglutide, tirzepatide, ` |
| Researcher 1 | `faers_top_reactions` | `{"start_year": 2020, "serious_only": false, "end_year": 2026, "drug": "semaglutide"}` |
| Researcher 1 | `faers_compare_drugs` | `{"reaction": "SUICIDAL IDEATION", "drugs": ["semaglutide", "tirzepatide", "liraglutide"]}` |

Full results: `tool_calls` in the /chat response.
</details>

### Same model, no tools and no system prompt

Because the FDA Adverse Event Reporting System (FAERS) is a dynamic database updated daily with self-reported data, the exact, live percentages shift constantly. However, several published pharmacovigilance studies and reviews by regulatory bodies (such as the FDA and the European Medicines Agency) have analyzed FAERS data to calculate these rates. 

Across all three drugs—semaglutide, tirzepatide, and liraglutide—the share of adverse event reports mentioning suicidal ideation is **extremely low, typically ranging from 0.1% to 0.5%** of each drug's total reports. 

Below is a comparative breakdown of how these three drugs compare based on pharmacovigilance data, regulatory evaluations, and scientific studies.

---

### 1. Semaglutide (Ozempic, Wegovy)
* **Approximate Share of Reports:** **~0.2% to 0.5%** of total FAERS reports.
* **Context:** Because semaglutide has experienced massive global popularity and intense media scrutiny, it has a very high overall volume of FAERS reports (well over 50,000 cumulative reports). Out of these, a few hundred mention suicidal ideation or self-harm. 
* **Stimulated Reporting:** Experts note that semaglutide’s data is highly subject to "stimulated reporting" (the *Weber Effect*), where heavy news coverage of a potential side effect prompts a surge in patients and doctors filing reports for that specific symptom, artificially inflating the share of reports.

### 2. Liraglutide (Victoza, Saxenda)
* **Approximate Share of Reports:** **~0.1% to 0.2%** of total FAERS reports.
* **Context:** Approved in 2010 (Victoza) and 2014 (Saxenda), liraglutide is an older, first-generation daily GLP-1 receptor agonist. Because it has been on the market much longer, its safety profile is highly mature. Despite having a massive cumulative database of adverse events, the percentage of reports mentioning suicidal thoughts has historically remained incredibly low. 

### 3. Tirzepatide (Mounjaro, Zepbound)
* **Approximate Share of Reports:** **~0.1% to 0.3%** of total FAERS reports.
* **Context:** As a newer dual-agonist (GLP-1/GIP) approved in 2022, tirzepatide has a smaller overall volume of historical reports in FAERS compared to semaglutide and liraglutide. However, initial disproportionality analyses of the FAERS database show that the proportion of suicidal ideation reports is similarly low, mirroring or falling slightly below that of semaglutide.

---

### Key Findings from Major Scientific and Regulatory Reviews

Because raw FAERS data cannot prove causation (anyone can submit a report, and reports often involve patients with pre-existing depression or those taking other medications), major medical institutions have conducted controlled studies to find the true risk.

#### 1. The FDA’s Official Position (January 2024)
Following a detailed review of FAERS reports of suicidal thoughts or actions associated with GLP-1 receptor agonists, the FDA issued a safety communication stating:
* **No causal link was found.** 
* The FDA noted that because the absolute number of these reports is very low, and because many reports contained confounding factors (such as a history of depression or life stressors), they could not establish that the drugs caused the suicidal thoughts.

#### 2. The European Medicines Agency (EMA) Review (April 2024)
The EMA’s Pharmacovigilance Risk Assessment Committee (PRAC) carried out an extensive review of non-clinical, clinical trial, and post-marketing surveillance data (including FAERS and European databases). 
* They concluded that **the available evidence does not support a causal association** between GLP-1 receptor agonists (including semaglutide and liraglutide) and suicidal or self-harming thoughts or actions.

#### 3. Large-Scale EHR Study (Published in *Nature Medicine*, Jan 2024)
To bypass the limitations of FAERS, researchers funded by the National Institutes of Health (NIH) analyzed electronic health records (EHRs) of over 240,000 overweight or obese patients. 
* They compared patients prescribed semaglutide to those prescribed non-GLP-1 weight-loss medications.
* **The result:** Patients taking semaglutide actually had a **49% to 73% *lower* risk of first-time or recurrent suicidal ideation** compared to patients taking other weight-loss drugs. Similar protective trends were observed when comparing semaglutide to other diabetes medications.

### Summary of FAERS Limitations
When comparing these percentages, epidemiologists emphasize that **FAERS data does not represent a clinical trial.** 
* **The Denominator Problem:** Millions of people take these drugs. A few hundred reports of suicidal ideation out of millions of users means the real-world occurrence rate is exceedingly low.
* **Baseline Rates:** In any population of millions of people (especially those dealing with chronic conditions like obesity and type 2 diabetes, which are statistically linked to higher rates of depression), a baseline number of people will experience suicidal thoughts regardless of the medication they are taking.


## 3. Has metformin been recalled since 2019, and why?

### Expected (computed directly from openFDA, no model)

65 recall records since 2019. By reason: NDMA or other nitrosamine impurity: 47; Storage temperature problem: 6; Foreign material or wrong pill in the bottle: 5; Sterility or manufacturing practice problem: 4; Failed dissolution or potency test: 2; Other impurity or contamination: 1. By year started: 2020: 44, 2021: 15, 2022: 1, 2023: 1, 2024: 1, 2025: 2, 2026: 1.

Source: `/drug/enforcement.json` (https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22metformin%22+OR+openfda.brand_name%3A%22metformin%22+OR+product_description%3A%22metformin%22%29+AND+recall_initiation_date%3A%5B20190101+TO+29991231%5D&limit=100)

### This agent

**Short answer:** Metformin has been recalled 65 times since 2019 ([openFDA Drug Recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22metformin%22+OR+openfda.brand_name%3A%22metformin%22+OR+product_description%3A%22metformin%22%29+AND+recall_initiation_date%3A%5B20190101+TO+29991231%5D&limit=100)). The primary reason for these recalls was the discovery of NDMA or other nitrosamine impurities ([openFDA Drug Recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22metformin%22+OR+openfda.brand_name%3A%22metformin%22+OR+product_description%3A%22metformin%22%29+AND+recall_initiation_date%3A%5B20190101+TO+29991231%5D&limit=100)).

### Metformin Recalls by Year

There were 65 total recalls for metformin since 2019, categorized by class as 62 Class II recalls and 3 Class III recalls ([openFDA Drug Recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22metformin%22+OR+openfda.brand_name%3A%22metformin%22+OR+product_description%3A%22metformin%22%29+AND+recall_initiation_date%3A%5B20190101+TO+29991231%5D&limit=100)). 

The table below breaks down the number of recalls that occurred each year, according to the FDA recall database ([openFDA Drug Recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22metformin%22+OR+openfda.brand_name%3A%22metformin%22+OR+product_description%3A%22metformin%22%29+AND+recall_initiation_date%3A%5B20190101+TO+29991231%5D&limit=100)).

| Year | Number of Recalls |
| :--- | :--- |
| 2020 | 44 |
| 2021 | 15 |
| 2022 | 1 |
| 2023 | 1 |
| 2024 | 1 |
| 2025 | 2 |
| 2026 | 1 |

### Reasons for the Recalls

Several different issues led to these recalls ([openFDA Drug Recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22metformin%22+OR+openfda.brand_name%3A%22metformin%22+OR+product_description%3A%22metformin%22%29+AND+recall_initiation_date%3A%5B20190101+TO+29991231%5D&limit=100)). The specific reasons and the number of recalls associated with each are listed below:

*   **NDMA or other nitrosamine impurity:** 47 recalls ([openFDA Drug Recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22metformin%22+OR+openfda.brand_name%3A%22metformin%22+OR+product_description%3A%22metformin%22%29+AND+recall_initiation_date%3A%5B20190101+TO+29991231%5D&limit=100)).
*   **Storage temperature problem:** 6 recalls ([openFDA Drug Recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22metformin%22+OR+openfda.brand_name%3A%22metformin%22+OR+product_description%3A%22metformin%22%29+AND+recall_initiation_date%3A%5B20190101+TO+29991231%5D&limit=100)).
*   **Foreign material or wrong pill in the bottle:** 5 recalls ([openFDA Drug Recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22metformin%22+OR+openfda.brand_name%3A%22metformin%22+OR+product_description%3A%22metformin%22%29+AND+recall_initiation_date%3A%5B20190101+TO+29991231%5D&limit=100)).
*   **Sterility or manufacturing practice problem:** 4 recalls ([openFDA Drug Recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22metformin%22+OR+openfda.brand_name%3A%22metformin%22+OR+product_description%3A%22metformin%22%29+AND+recall_initiation_date%3A%5B20190101+TO+29991231%5D&limit=100)).
*   **Failed dissolution or potency test:** 2 recalls ([openFDA Drug Recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22metformin%22+OR+openfda.brand_name%3A%22metformin%22+OR+product_description%3A%22metformin%22%29+AND+recall_initiation_date%3A%5B20190101+TO+29991231%5D&limit=100)).
*   **Other impurity or contamination:** 1 recall ([openFDA Drug Recalls](https://api.fda.gov/drug/enforcement.json?search=%28openfda.generic_name%3A%22metformin%22+OR+openfda.brand_name%3A%22metformin%22+OR+product_description%3A%22metformin%22%29+AND+recall_initiation_date%3A%5B20190101+TO+29991231%5D&limit=100)).

### What this data can't tell you

A recall is about a batch, not proof anyone was harmed. Older or smaller recalls may name the drug differently. Additionally, the provided findings do not answer which specific manufacturers, brand names, or lot numbers were associated with these recalls.

_Not medical advice: talk to your doctor or pharmacist._

<details><summary>Trace: 3 tool calls, 1 researchers</summary>

| Agent | Tool | Arguments |
| --- | --- | --- |
| Lead | `resolve_drug_name` | `{"name": "metformin"}` |
| Lead | `research` | `{"task": "FDA recalls of metformin since 2019 and the reasons for those recalls (openFDA)"}` |
| Researcher 1 | `drug_recalls` | `{"drug": "metformin", "start_year": 2019}` |

Full results: `tool_calls` in the /chat response.
</details>

### Same model, no tools and no system prompt

Yes, there have been significant recalls of metformin since late 2019. 

The recalls primarily affected certain **extended-release (ER)** formulations of the drug. The immediate-release (IR) versions of metformin, which are the most commonly prescribed, were generally not affected.

Here is a detailed breakdown of why these recalls occurred and what you need to know.

---

### Why Was Metformin Recalled?
The recalls were triggered by the detection of unacceptable levels of a chemical impurity called **NDMA (N-nitrosodimethylamine)**. 

* **What is NDMA?** NDMA is an organic chemical that is classified as a "probable human carcinogen" (a substance that could increase the risk of cancer) based on laboratory tests. 
* **Where does it come from?** NDMA is a common environmental contaminant found in low levels in water and foods (such as cured meats, beer, and dairy products). 
* **Why was it in the medication?** The NDMA found in metformin was not an active ingredient. Instead, it was an impurity that likely formed during the manufacturing process, during storage, or due to the chemical structure of the drug breakdown over time under certain conditions.

### Timeline of the Recalls
* **Late 2019:** The FDA became aware of NDMA in metformin in other countries and began testing samples in the United States.
* **May 2020:** The FDA announced that its testing revealed NDMA levels above the acceptable daily intake limit in several lots of extended-release (ER) metformin. The agency asked five pharmaceutical companies to voluntarily recall their affected products.
* **2020–2021:** Multiple manufacturers voluntarily recalled specific lots of Metformin Hydrochloride Extended-Release tablets (primarily 500 mg and 750 mg strengths). Recalling companies included:
  * Amneal Pharmaceuticals
  * Apotex Corp.
  * Lupin Pharmaceuticals
  * Marksans Pharma Limited
  * Teva Pharmaceuticals
  * Nostrum Laboratories

### Important Information for Patients
If you or a loved one takes metformin, it is important to keep the following medical advice in mind:

1. **Do NOT stop taking your metformin without consulting a doctor first.** The risk of leaving type 2 diabetes untreated (which can lead to dangerously high blood sugar, heart disease, kidney damage, and blindness) is far more immediate and dangerous than the potential low risk associated with the NDMA impurity.
2. **Check your bottle:** Look at your prescription bottle to see if your medication is "Extended-Release" (often labeled as ER, XR, or XL). If it is, check the manufacturer's name.
3. **Talk to your pharmacist:** Your pharmacist can quickly look up your prescription history to tell you if the specific lot number of your medication was part of any recall. If it was, they can easily swap it for an unaffected lot or a different manufacturer.
