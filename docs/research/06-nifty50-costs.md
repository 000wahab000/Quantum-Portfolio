# NIFTY 50: constituents, delivery trading costs, risk-free rate, yfinance caveats

Research date: 2026-10-08. Every figure is tied to a source in the Sources section, or marked [unverified].

## 1. Current NIFTY 50 constituents

**As-of:** The constituents CSV was downloaded on 2026-10-08 with curl from https://niftyindices.com/IndexConstituent/ind_nifty50list.csv. The file has no internal date. Its membership matches the September 2026 semi-annual review, effective 2026-09-30 (NSE Indices press release dated 10 Aug 2026, ind_prs10082026.pdf). The file has 50 data rows, no duplicate symbols, and no uncertain membership rows.

The `sector` column is the NSE "Industry" field from the CSV, not a GICS sector.

```csv
symbol,yf_ticker,name,sector
ADANIENT,ADANIENT.NS,Adani Enterprises Ltd.,Metals & Mining
ADANIPORTS,ADANIPORTS.NS,Adani Ports and Special Economic Zone Ltd.,Services
APOLLOHOSP,APOLLOHOSP.NS,Apollo Hospitals Enterprise Ltd.,Healthcare
ASIANPAINT,ASIANPAINT.NS,Asian Paints Ltd.,Consumer Durables
AXISBANK,AXISBANK.NS,Axis Bank Ltd.,Financial Services
BSE,BSE.NS,BSE Ltd.,Financial Services
BAJAJ-AUTO,BAJAJ-AUTO.NS,Bajaj Auto Ltd.,Automobile and Auto Components
BAJFINANCE,BAJFINANCE.NS,Bajaj Finance Ltd.,Financial Services
BAJAJFINSV,BAJAJFINSV.NS,Bajaj Finserv Ltd.,Financial Services
BEL,BEL.NS,Bharat Electronics Ltd.,Capital Goods
BHARTIARTL,BHARTIARTL.NS,Bharti Airtel Ltd.,Telecommunication
CIPLA,CIPLA.NS,Cipla Ltd.,Healthcare
COALINDIA,COALINDIA.NS,Coal India Ltd.,Oil Gas & Consumable Fuels
DRREDDY,DRREDDY.NS,Dr. Reddy's Laboratories Ltd.,Healthcare
EICHERMOT,EICHERMOT.NS,Eicher Motors Ltd.,Automobile and Auto Components
ETERNAL,ETERNAL.NS,Eternal Ltd.,Consumer Services
GRASIM,GRASIM.NS,Grasim Industries Ltd.,Construction Materials
HCLTECH,HCLTECH.NS,HCL Technologies Ltd.,Information Technology
HDFCBANK,HDFCBANK.NS,HDFC Bank Ltd.,Financial Services
HDFCLIFE,HDFCLIFE.NS,HDFC Life Insurance Company Ltd.,Financial Services
HINDALCO,HINDALCO.NS,Hindalco Industries Ltd.,Metals & Mining
HINDUNILVR,HINDUNILVR.NS,Hindustan Unilever Ltd.,Fast Moving Consumer Goods
ICICIBANK,ICICIBANK.NS,ICICI Bank Ltd.,Financial Services
ITC,ITC.NS,ITC Ltd.,Fast Moving Consumer Goods
INFY,INFY.NS,Infosys Ltd.,Information Technology
INDIGO,INDIGO.NS,InterGlobe Aviation Ltd.,Services
JSWSTEEL,JSWSTEEL.NS,JSW Steel Ltd.,Metals & Mining
JIOFIN,JIOFIN.NS,Jio Financial Services Ltd.,Financial Services
KOTAKBANK,KOTAKBANK.NS,Kotak Mahindra Bank Ltd.,Financial Services
LT,LT.NS,Larsen & Toubro Ltd.,Construction
M&M,M&M.NS,Mahindra & Mahindra Ltd.,Automobile and Auto Components
MARUTI,MARUTI.NS,Maruti Suzuki India Ltd.,Automobile and Auto Components
MAXHEALTH,MAXHEALTH.NS,Max Healthcare Institute Ltd.,Healthcare
NTPC,NTPC.NS,NTPC Ltd.,Power
NESTLEIND,NESTLEIND.NS,Nestle India Ltd.,Fast Moving Consumer Goods
ONGC,ONGC.NS,Oil & Natural Gas Corporation Ltd.,Oil Gas & Consumable Fuels
POWERGRID,POWERGRID.NS,Power Grid Corporation of India Ltd.,Power
RELIANCE,RELIANCE.NS,Reliance Industries Ltd.,Oil Gas & Consumable Fuels
SBILIFE,SBILIFE.NS,SBI Life Insurance Company Ltd.,Financial Services
SHRIRAMFIN,SHRIRAMFIN.NS,Shriram Finance Ltd.,Financial Services
SBIN,SBIN.NS,State Bank of India,Financial Services
SUNPHARMA,SUNPHARMA.NS,Sun Pharmaceutical Industries Ltd.,Healthcare
TCS,TCS.NS,Tata Consultancy Services Ltd.,Information Technology
TATACONSUM,TATACONSUM.NS,Tata Consumer Products Ltd.,Fast Moving Consumer Goods
TMPV,TMPV.NS,Tata Motors Passenger Vehicles Ltd.,Automobile and Auto Components
TATASTEEL,TATASTEEL.NS,Tata Steel Ltd.,Metals & Mining
TECHM,TECHM.NS,Tech Mahindra Ltd.,Information Technology
TITAN,TITAN.NS,Titan Company Ltd.,Consumer Durables
TRENT,TRENT.NS,Trent Ltd.,Consumer Services
ULTRACEMCO,ULTRACEMCO.NS,UltraTech Cement Ltd.,Construction Materials
```

**Rows to watch (membership is confirmed; these are data caveats, see section 4):** TMPV (demerger price break in pre-Oct-2025 history), ETERNAL (formerly Zomato), BSE (joined 30 Sep 2026).

### Membership changes, last ~2 years (NSE Indices press releases)

| Effective (last close before) | NSE PR date | Added | Removed | Notes |
|---|---|---|---|---|
| 30 Sep 2024 (27 Sep) | 23 Aug 2024 | Bharat Electronics (BEL), Trent (TRENT) | Divi's Laboratories (DIVISLAB), LTIMindtree (LTIM) | Edge of the window |
| 28 Mar 2025 (27 Mar) | 21 Feb 2025 | Jio Financial Services (JIOFIN), Zomato, now Eternal (ETERNAL) | Bharat Petroleum (BPCL), Britannia (BRITANNIA) | |
| 30 Sep 2025 (29 Sep) | 22 Aug 2025 | InterGlobe Aviation (INDIGO), Max Healthcare (MAXHEALTH) | Hero MotoCorp (HEROMOTOCO), IndusInd Bank (INDUSINDBK) | |
| 14 Oct 2025 (demerger) | NSE PR 13 Nov 2025 | None | None | Tata Motors renamed TMPV (news: effective 24 Oct 2025). TMPV is in the Sep 2026 CSV, and no PR read removed it. The CV arm (TMCV, formerly TML Commercial Vehicles) was given dummy symbol DUMMYTATAM from 14 Oct 2025, then excluded from Nifty indices after its 12 Nov 2025 listing. The PR table lists "Nifty 50" among them, so TMCV was never a real Nifty 50 member. |
| 30 Mar 2026 (27 Mar) | 23 Feb 2026 | None | None | NSE PR: "No changes are being made in Nifty 50 and Nifty50 Equal Weight indices." |
| 30 Sep 2026 (29 Sep) | 10 Aug 2026 | BSE Ltd (BSE) | Wipro (WIPRO) | Wipro moves to Nifty Next 50 (news). |

Totals in the window: 7 adds and 7 drops, plus the TMPV corporate event.

**Survivorship bias:** A backtest that uses the current 50 for 2024 to 2026 would hold BSE, INDIGO, MAXHEALTH, JIOFIN, ETERNAL, TRENT and BEL before they joined, and would omit the seven removed names. Build point-in-time membership from this table. Events before Sep 2024 were not reconstructed here.

## 2. Delivery transaction costs

| Component | Rate | Applies to | Source (as-of) | Status |
|---|---|---|---|---|
| Brokerage | 0 | Buy and sell | Zerodha charges page (fetched 8 Oct 2026; page shows no effective date) | Broker-stated |
| STT | 0.100% of value | Buy and sell | NSE "SEBI Turnover Fees, STT and Other levies" (page updated 17 Apr 2026; rates w.e.f. 1 Apr 2026; delivery rate 0.100% on purchase and on sale) | Confirmed (NSE) |
| Exchange transaction charge (NSE, incl. IPFT) | 0.00307% (Rs 307 per crore) | Buy and sell | NSE circular FA/73061, 27 Feb 2026, effective 1 Mar 2026: transaction charge Rs 306.99 plus IPFT Rs 0.01 = Rs 307 per crore each side. Zerodha page also shows 0.00307%. | Confirmed (NSE circular) |
| SEBI turnover fee | 0.0001% (Rs 10 per crore) | Buy and sell | NSE page | Confirmed (NSE) |
| Stamp duty (delivery) | 0.015% (Rs 1,500 per crore) | Buyer only | NSE page | Confirmed (NSE) |
| GST | 18% | Base per Zerodha: brokerage + exchange charge + SEBI fee | NSE page gives 18% for broker services; base from Zerodha | Rate confirmed; base broker-stated |
| DP charge | Rs 15.34 per scrip, per sell day, irrespective of quantity (CDSL Rs 3.5 + Zerodha Rs 9.5 + GST Rs 2.34) | Sell only | Zerodha charges page | Broker-stated [unverified against CDSL] |

### Arithmetic for a Rs 1,00,000 trade

Buy leg:
- STT = 0.1% x 100,000 = 100.00
- Exchange = 0.00307% x 100,000 = 3.07
- SEBI = 0.0001% x 100,000 = 0.10
- Stamp = 0.015% x 100,000 = 15.00
- GST = 18% x (0 + 3.07 + 0.10) = 0.57
- Total = 118.74, which is **0.1187%**

Sell leg:
- STT = 100.00; exchange = 3.07; SEBI = 0.10; GST = 0.57 (no stamp duty on sell)
- Subtotal before DP = 103.74, which is **0.1037%**
- DP = 15.34 (fixed per scrip per sell day)
- Total including DP = 119.08, which is 0.1191%

Round trip (buy Rs 1,00,000, then sell Rs 1,00,000):
- Proportional only: 118.74 + 103.74 = 222.48, which is **0.2225%**
- Including one DP charge: 222.48 + 15.34 = 237.82, which is **0.2378%**

### Simple proportional cost model

- c_buy = 0.001187 (0.1187%)
- c_sell = 0.001037 (0.1037%)
- DP = Rs 15.34 fixed per sell per scrip. This is 0.0153% at Rs 1 lakh, so it matters for small trades only.
- Round trip is about 0.22% proportional, or about 0.24% with one DP charge at Rs 1 lakh.

Not modelled: market impact, bid-ask spread, slippage, and capital gains tax.

## 3. Risk-free rate

- **91-day T-bill cut-off yield: 5.5747%.** Source: the RBI homepage T-bill block, displayed "as at 1.00 pm, 8 Oct 2026", with the footnote "cut-off at the last auction". The block does not show the auction date [auction date unverified]. The same block shows 182-day 6.0999% and 364-day 6.2869%.
- **RBI policy repo rate: 5.50%.** The MPC raised it by 25 bps on 7 Oct 2026 (press release 2026-2027/1264, dated 7 Oct 2026). The stance changed to "calibrated tightening". SDF is 5.25%, and MSF and Bank Rate are 5.75%. Next MPC meeting: 2 to 4 Dec 2026.
- Superseded: 5.2640% for the 27 Aug 2026 91-day auction, from a search snippet. Not used.

**Recommendation:** rf = 5.57% per year (use 0.0557 in the Sharpe). At 252 trading days, the per-day rate is 0.0557 / 252 = 0.0221%. Use the same return frequency and convention in the numerator and denominator.

## 4. yfinance and .NS tickers

Test run on 2026-10-08 with yfinance 1.5.1 on Python 3.13.14. One `yf.download` call, `auto_adjust=True`, `start=2024-01-01`, covering the 50 CSV tickers plus 12 legacy and renamed symbols. The script is in the session scratchpad and is not in the repo.

- **All 50 CSV tickers returned data.** 49 have 690 trading-day rows. INDIGO.NS has 689, one fewer, not investigated.
- **Failing:** TATAMOTORS.NS (0 rows), ZOMATO.NS (0 rows), LTIM.NS (0 rows). Use ETERNAL.NS for Zomato. The cause of the LTIM failure is not explained here [unverified].
- **Legacy symbols still returning data from 2024:** WIPRO.NS, BPCL.NS, BRITANNIA.NS, HEROMOTOCO.NS and INDUSINDBK.NS (690 rows each), DIVISLAB.NS (689 rows). Use these for survivorship-aware backtests.
- **TMPV.NS price break, a data trap:** The series from 2024 is the pre-demerger Tata Motors line. The close falls from 655.31 on 13 Oct 2025 to 392.20 on 14 Oct 2025 with `auto_adjust=True`, or from 660.75 to 395.45 raw. That is -40.1%, a demerger effect, not a market move. yfinance does not adjust for it. Fix: start the TMPV series on 2025-10-14, or apply a demerger adjustment factor. I did not compute that factor because it needs NSE's demerger ratio [unverified].
- **TMCV.NS** (the CV arm, not in NIFTY 50) has data only from its 12 Nov 2025 listing (230 rows).
- **Rate limits:** The single batch call for about 62 tickers hit no 429 or throttling errors. General reports of "Too Many Requests" exist, but those came from low-authority sites. Batch with `yf.download` and space out requests.
- **Old claim contradicted:** An older forum post said BAJAJ-AUTO.NS returns no data. This run returned 690 rows.
- **Not tested:** history before 2024, adjustments beyond `auto_adjust`, and intraday data. My search found no 2026 report of .NS-specific breakage beyond the rename and demerger items above.

## Sources

1. NIFTY 50 constituents CSV, NSE Indices / niftyindices.com, retrieved 2026-10-08: https://niftyindices.com/IndexConstituent/ind_nifty50list.csv
2. NSE Indices press release dated 10 Aug 2026, replacements effective 30 Sep 2026: https://niftyindices.com/Press_Release/ind_prs10082026.pdf
3. NSE Indices press release dated 23 Feb 2026, effective 30 Mar 2026: https://niftyindices.com/Press_Release/ind_prs23022026.pdf
4. NSE Indices press release dated 22 Aug 2025, effective 30 Sep 2025: https://niftyindices.com/Press_Release/ind_prs22082025.pdf
5. NSE Indices press release dated 21 Feb 2025, effective 28 Mar 2025: https://nsearchives.nseindia.com/web/sites/default/files/2025-02/ind_prs21022025.pdf
6. NSE Indices press release dated 23 Aug 2024, effective 30 Sep 2024: https://niftyindices.com/Press_Release/ind_prs23082024.pdf
7. NSE Indices press release dated 13 Nov 2025, exclusion of Tata Motors Ltd (TMCV): https://niftyindices.com/Press_Release/ind_prs13112025.pdf
8. Zerodha charges page, fetched 2026-10-08: https://zerodha.com/charges
9. NSE, "SEBI Turnover Fees, STT and Other levies" (updated 17/04/2026, viewed 2026-10-08): https://www.nseindia.com/static/invest/first-time-investor-sebi-turnover-fees-stt-other-levies
10. NSE circular NSE/FA/73061, "Revision in Transaction Charges", 27 Feb 2026: https://nsearchives.nseindia.com/content/circulars/FA73061.pdf
11. RBI press release, Resolution of the Monetary Policy Committee, 5 to 7 Oct 2026 (dated 7 Oct 2026): https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=63742
12. RBI homepage T-bill and policy-rate block, as at 1.00 pm 8 Oct 2026 (fetched via https://website.rbi.org.in/web/rbi/-/press-releases/91-days-treasury-bills-auction-result-cut-off-47337, which returned the homepage): https://rbi.org.in/
13. Zerodha Market Intel bulletin 431402, Tata Motors symbol change (secondary, 23 Oct 2025): https://zerodha.com/marketintel/bulletin/431402/change-in-stock-name-and-symbol-for-tata-motors-ltd
14. Bajaj Broking, "Nifty Rejig: BSE Replaces Wipro in Nifty 50" (secondary, for Wipro moving to Nifty Next 50): https://www.bajajbroking.in/share-market-news/nifty-rejig-bse-replaces-wipro-in-nifty-50
15. Local yfinance 1.5.1 run, 2026-10-08 (no URL; script in session scratchpad)
