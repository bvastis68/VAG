---
name: financial-plan-ca
description: Build or update a financial plan for Canadian and cross-border clients — retirement and decumulation projections, RESP education funding, estate and probate planning, corporate/Holdco integration, and cash flow analysis. Use for new client onboarding, annual plan reviews, or scenario modeling in the Vastis practice. Triggers on "financial plan", "retirement plan", "can I retire", "decumulation", "RRSP meltdown", "OAS clawback", "RRIF minimum", "education funding", "RESP", "estate plan", "probate", "cash flow analysis", or "plan update".
---

# Financial Plan — Canadian & Cross-Border

Replaces the U.S.-default `financial-plan` skill for this practice. That skill
asks for 401(k), IRA and Social Security. This one asks the questions that
actually apply to a Vastis household.

Defer to `firm-context` for account taxonomy, house views, and style. Layer U.S.
treatment only for genuine cross-border files — it is not the default.

## Input Discipline — Read First

This plan is only as honest as its inputs. Three rules:

1. **Never invent return, volatility or correlation assumptions.** Use RBC's
   current capital market assumptions, or assumptions the advisor supplies.
   State them in the plan.
2. **Never state an indexed figure from memory.** OAS recovery-tax threshold,
   TFSA and RRSP contribution limits, CPP/OAS maximums, YMPE, and the passive-
   income threshold are indexed or legislated and move. Confirm the current-year
   number before it goes in a deliverable. Mechanics below are stable; the
   dollar figures are not.
3. **Monte Carlo means an actual simulation.** Run the computation — do not
   produce a probability-of-success figure by estimation. If the inputs aren't
   available, say so rather than producing a number.

## Step 1: Client Profile

- **Demographics**: Ages, spouse age, dependents, province of residence,
  life expectancy assumption (plan to 95 as default; longer for healthy UHNW).
- **Residency & citizenship**: Canadian resident? U.S. person? Dual citizen?
  Snowbird with U.S. day counts? Drives everything downstream.
- **Employment**: Income, bonus, expected raises, target retirement age,
  employer pension (DB or DC), business ownership.
- **Accounts** — balances, allocation, and contribution room:
  - RRSP / Spousal RRSP
  - RRIF (if already converted)
  - TFSA
  - RESP (per beneficiary, with CESG received to date)
  - LIRA / LIF
  - Non-registered / taxable
  - Corporate / Holdco
  - Trusts (family, alter-ego, joint-partner)
  - Cross-border only: IRA / Roth / 401(k)
- **Government benefits**: CPP (or QPP) statement of contributions, OAS
  eligibility and years of Canadian residence after 18.
- **Expenses**: Current spending, expected changes (mortgage payoff, kids
  independent, care costs).
- **Liabilities**: Mortgage, investment loans, IFA facilities, corporate debt.
- **Insurance**: Life (personal and corporate-owned), disability, critical
  illness, LTC.
- **Estate**: Wills (and separate wills for private-company shares where the
  province allows), POAs, beneficiary and successor-holder designations,
  gifting, philanthropic intent.

## Step 2: Cash Flow Analysis

| Year | Age | Employment Income | Investment Income | Taxes | Living Expenses | Savings | Net |
|------|-----|-------------------|-------------------|-------|-----------------|---------|-----|

Inputs:
- Inflation assumption (2–3% default; model higher for care costs).
- **Marginal rates by income type** — Canadian rates differ sharply across
  salary, eligible dividends, non-eligible dividends, capital gains and
  interest. Do not blend them into one effective rate.
- Provincial rates, not just federal.
- Where savings are directed: RRSP, TFSA, non-registered, or corporate.

## Step 3: Retirement Projections

### Accumulation

- Current portfolio by account type.
- Annual contributions: RRSP (18% of prior-year earned income to the annual
  limit, plus carry-forward room), TFSA (annual limit plus unused room and
  prior withdrawals), non-registered, corporate retained earnings.
- Expected return by asset class — from RBC CMAs, including the alternatives
  sleeve at its target weight. Do not benchmark to a 60/40.
- **Monte Carlo**: probability of success across spending levels. Run it.

### Decumulation — the part that matters

- **RRSP → RRIF conversion**: mandatory by December 31 of the year the client
  turns 71. Model the conversion year explicitly.
- **RRIF minimums**: age-based factors, calculated on January 1 balance.
  These are *minimums*, not U.S.-style RMDs — the mechanics and the ages
  differ. A younger spouse's age may be elected to reduce the factor.
- **CPP timing**: start between 60 and 70. Early = permanent reduction,
  deferral = permanent enhancement. Model 60 / 65 / 70.
- **OAS timing and clawback**: start 65–70. The recovery tax claws back 15%
  of net income above the threshold, to full elimination at the upper bound.
  **This is the single biggest planning lever in most Canadian retirements** —
  and the one the U.S. skill has no concept of.
- **Withdrawal sequencing**: model the order, don't assume it.
  - Drawing RRSP/RRIF early can reduce forced income later, lowering lifetime
    OAS clawback and the tax hit on the estate's final return.
  - TFSA generally last — tax-free growth, and it passes to a successor holder
    outside the estate.
  - Corporate money needs integration analysis: salary vs. dividend, CDA
    balance, passive income grinding the small business deduction.
- **Pension income splitting**: up to 50% of eligible pension income with a
  spouse from 65 (RRIF income qualifies; RRSP withdrawals do not).
  CPP sharing is separate and also available.
- **RRSP meltdown**: where suitable, deliberate early RRSP drawdown — often
  paired with an investment loan or IFA — to shift income out of the high-rate
  terminal year. Model it; flag it for KPMG.

### Key Output

- Projected portfolio at retirement, by account type (not just a single total —
  the tax character matters).
- Sustainable spending in after-tax dollars.
- Probability of success (target >85%).
- Lifetime OAS retained vs. clawed back under each sequencing scenario.
- Estate value after the terminal-return tax hit.

## Step 4: Goal-Specific Analysis

### Education Funding — RESP

- Beneficiary ages and target start.
- Current RESP balance and **CESG received to date** (20% federal match on
  contributions, annual and lifetime caps, with carry-forward of one prior
  year's room). Confirm current figures.
- Provincial incentives where applicable.
- Contribution schedule to maximize grant rather than front-load past it.
- Withdrawal mechanics: EAP (grant + growth, taxable to the student) vs.
  return of contributions (tax-free). Sequence to use the student's low bracket.
- Over-contribution penalties; what happens if the child doesn't attend —
  AIP, RRSP transfer room, grant repayment.
- Cross-border flag: RESPs are not recognized by the IRS. For U.S. persons,
  this is a 3520/3520-A reporting problem. Raise it before funding, not after.

### Estate Planning — Canadian Mechanics

**Canada has no estate tax.** Do not import the U.S. framing of exemptions and
federal/state estate tax. The Canadian exposures are different:

- **Deemed disposition at death**: the entire portfolio is treated as sold at
  fair market value. This is usually the largest single tax event in a client's
  life. Model it.
- **Spousal rollover**: deferral to the surviving spouse or a qualifying
  spousal trust. The bill lands on the second death — plan to that date.
- **Registered accounts**: RRSP/RRIF fully into income on the terminal return
  absent a qualifying rollover. Often the top marginal rate on the full balance.
- **Probate fees**: provincial and variable (Ontario's estate administration
  tax is material above the first tier; Alberta's is capped and nominal).
  Structure accordingly — multiple wills, joint ownership with care,
  beneficiary designations, alter-ego or joint-partner trusts from age 65.
- **U.S.-situs assets**: U.S. estate tax can apply to Canadians holding U.S.
  stocks or U.S. real estate. Treaty relief is prorated and not automatic.
  Quantify it; structure around it.
- **Corporate estates**: post-mortem planning (pipeline, loss carryback),
  CDA extraction, double-tax risk on private company shares.
- **IFA (Insurance Financing Arrangements)**: for the right UHNW client, the
  tool that funds the terminal tax bill without liquidating the portfolio.
  Treat under estate and risk management — not as an investment product.
- Charitable giving: donation of appreciated securities in kind eliminates the
  capital gain; gifts by will and designation.

### Risk Management

- Life insurance needs: terminal tax liability, debt payoff, income
  replacement, estate equalization among children.
- Corporate-owned vs. personally-owned policy — CDA credit on death.
- Disability and critical illness.
- Long-term care — provincial coverage is partial; model the shortfall.
- Umbrella liability.

## Step 5: Scenario Modeling

| Scenario | P(Success) | Estate After Tax | Lifetime OAS Retained | Notes |
|----------|-----------|------------------|-----------------------|-------|
| Base case | | | | |
| Retire 2 years early | | | | |
| 20% drawdown in year 1 | | | | |
| Spending +20% | | | | |
| CPP/OAS deferred to 70 | | | | |
| RRSP meltdown from 60 | | | | |
| Surviving spouse to 95 | | | | |
| LTC event, 4 years | | | | |

Sequence-of-returns risk deserves its own scenario. A poor first five years of
decumulation does more damage than the same loss a decade later — show it.

## Step 6: Recommendations

Prioritized, with owners (Billy / Sydney / Jason):

1. Contribution and savings changes — RRSP vs. TFSA vs. corporate.
2. Asset location across registered, taxable and corporate accounts.
3. Decumulation sequence and CPP/OAS start ages.
4. Alternatives sleeve toward the 20–30% target where suitable and eligible.
5. Tax-loss harvesting on taxable sleeves — superficial loss rule governs,
   not the IRS wash-sale rule.
6. Insurance gaps, including terminal tax funding.
7. Estate document and beneficiary review.
8. Items staged for KPMG sign-off.

## Step 7: Output

- Plan document (15–25 pages) — client-facing layer plain, internal layer technical.
- Cash flow and decumulation projection (Excel).
- Retirement and estate-value charts.
- Scenario comparison table.
- Action checklist with owners and dates.

## Cross-Border Overlay

Apply only where residency or citizenship calls for it:

- Coordinate CPP/OAS with U.S. Social Security; the totalization agreement
  and treaty article govern.
- IRA/Roth/401(k) held by a Canadian resident — treaty deferral, withholding,
  and Canadian reporting.
- TFSA: not recognized by the IRS; 3520/3520-A exposure for U.S. persons.
  Often the wrong account for that client entirely.
- PFIC treatment of Canadian mutual funds and ETFs for U.S. persons.
- T1135 foreign property reporting; FBAR and Form 8938.
- Departure tax on ceasing Canadian residency; treaty tie-breakers.
- Snowbird day counts — substantial presence test and closer connection.

## Notes

- Plans are living documents. Review annually and after any major life event.
- Be conservative on returns. Overestimating gives false confidence, and the
  client remembers the number.
- In Canada the decumulation *sequence* is often worth more than the return
  assumption. Model it properly.
- Never blend income types into a single tax rate.
- A plan that only works in the base case is not a plan.
- Compliance: CIRO suitability applies. Nothing here is advice until reviewed
  and signed off; client-facing material goes through RBC DS compliance.
