"""Bank SMS templates and locale lists for generate_synth.py."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Locale:
    firsts: tuple[str, ...]
    surnames: tuple[str, ...]
    shops: tuple[str, ...]
    brands: tuple[str, ...]


@dataclass(frozen=True)
class Template:
    key: str
    bank: str
    country: str
    currency: str
    sender_core: str
    txn_type: str
    body: str
    required: tuple[str, ...]
    one_word_merchant: bool = False
    merchant_upper: bool = False


LOCALES: dict[str, Locale] = {
    "India": Locale(
        ("Ravi", "Priya", "Ankit", "Neha", "Rahul", "Pooja", "Arjun", "Meera"),
        ("Sharma", "Patel", "Verma", "Gupta", "Singh", "Kumar", "Reddy", "Iyer"),
        ("Kirana Store", "Medical Store", "Sweets Corner", "Tea Stall", "Mobile Shop"),
        ("Amazon Pay", "Swiggy", "Zomato", "IRCTC", "PhonePe", "Blinkit"),
    ),
    "United States": Locale(
        ("James", "Maria", "Chris", "Ashley", "David", "Emily"),
        ("Johnson", "Williams", "Brown", "Garcia", "Miller", "Davis"),
        ("Grocery", "Pharmacy", "Diner", "Gas Station", "Hardware"),
        ("Starbucks", "Amazon", "Walmart", "Uber", "Target", "Costco"),
    ),
    "UAE": Locale(
        ("Omar", "Fatima", "Hassan", "Layla", "Yusuf", "Noor"),
        ("Al Maktoum", "Al Nahyan", "Khan", "Rahman", "Hassan", "Ali"),
        ("Supermarket", "Pharmacy", "Cafe", "Electronics", "Salon"),
        ("Carrefour", "ADNOC", "Noon", "LuLu", "Careem", "Spinneys"),
    ),
    "Saudi Arabia": Locale(
        ("Fahad", "Aisha", "Majid", "Huda", "Sultan", "Noura"),
        ("Al Saud", "Al Harbi", "Al Otaibi", "Al Qahtani", "Al Ghamdi"),
        ("Pharmacy", "Bakery", "Market", "Fuel Station"),
        ("Panda", "Jarir", "STC", "Tamimi", "HungerStation"),
    ),
    "Ethiopia": Locale(
        ("Abebe", "Mekdes", "Dawit", "Hanna", "Yonas", "Selam"),
        ("Bekele", "Tesfaye", "Haile", "Alemu", "Kebede"),
        ("Mini Market", "Cafe", "Pharmacy", "Taxi Stand"),
        ("Ethio Telecom", "Dashen Super", "Abyssinia"),
    ),
    "Tanzania": Locale(
        ("Juma", "Amina", "Baraka", "Neema", "Hassani"),
        ("Mwangi", "Ngowi", "Kimaro", "Mushi", "Lyimo"),
        ("Duka", "Pharmacy", "Cafe", "Market"),
        ("Vodacom", "Shoppers", "Azam"),
    ),
    "Nigeria": Locale(
        ("Chinedu", "Aisha", "Tunde", "Ngozi", "Emeka", "Blessing"),
        ("Okafor", "Adeyemi", "Balogun", "Nwachukwu", "Ibrahim"),
        ("Market", "Pharmacy", "POS Agent", "Restaurant"),
        ("Jumia", "GTBank Transfer", "DSTV", "Uber NG"),
    ),
    "Nepal": Locale(
        ("Suman", "Anita", "Bikash", "Sita", "Ramesh"),
        ("Shrestha", "Gurung", "Tamang", "Adhikari", "Karki"),
        ("Pasal", "Pharmacy", "Cafe", "Mart"),
        ("eSewa", "Khalti", "Bhatbhateni"),
    ),
    "Egypt": Locale(
        ("Omar", "Mona", "Karim", "Yasmin", "Hassan"),
        ("Hassan", "Ibrahim", "Farouk", "Saleh", "Nour"),
        ("Pharmacy", "Cafe", "Market", "Fuel Station"),
        ("Fawry", "Carrefour EG", "Uber EG"),
    ),
    "Kenya": Locale(
        ("Kamau", "Wanjiku", "Otieno", "Achieng", "Mwangi"),
        ("Omondi", "Njeri", "Kipchoge", "Wambui", "Odhiambo"),
        ("Duka", "Pharmacy", "Kiosk", "Matatu"),
        ("Safaricom", "Naivas", "Java House", "Uber KE"),
    ),
    "Bangladesh": Locale(
        ("Rahim", "Fatema", "Karim", "Nusrat", "Hasan"),
        ("Rahman", "Ahmed", "Chowdhury", "Islam", "Hossain"),
        ("Dokan", "Pharmacy", "Cafe"),
        ("bKash Agent", "Grameenphone", "Unimart"),
    ),
    "Oman": Locale(
        ("Said", "Amal", "Nasser", "Maryam", "Khalid"),
        ("Al Busaidi", "Al Balushi", "Al Hinai", "Al Zadjali"),
        ("Pharmacy", "Cafe", "Hypermarket"),
        ("Ooredoo", "Carrefour OM", "Shell Oman"),
    ),
    "Pakistan": Locale(
        ("Ali", "Ayesha", "Bilal", "Hina", "Usman"),
        ("Khan", "Malik", "Sheikh", "Raza", "Qureshi"),
        ("General Store", "Pharmacy", "Cafe"),
        ("JazzCash", "Daraz", "PSO"),
    ),
    "Sri Lanka": Locale(
        ("Nimal", "Sanduni", "Kasun", "Ishara", "Tharindu"),
        ("Perera", "Fernando", "Silva", "Jayawardena"),
        ("Pharmacy", "Cafe", "Grocery"),
        ("Dialog", "Keells", "PickMe"),
    ),
    "Turkey": Locale(
        ("Mehmet", "Ayse", "Emre", "Elif", "Can"),
        ("Yilmaz", "Demir", "Kaya", "Celik", "Sahin"),
        ("Market", "Eczane", "Cafe"),
        ("BIM", "A101", "Trendyol"),
    ),
    "Russia": Locale(
        ("Ivan", "Anna", "Dmitry", "Olga", "Sergei"),
        ("Petrov", "Ivanov", "Smirnov", "Volkov"),
        ("Magazin", "Apteka", "Kafe"),
        ("Wildberries", "Yandex", "Ozon"),
    ),
    "Czech Republic": Locale(
        ("Jan", "Petra", "Tomas", "Eva", "Lukas"),
        ("Novak", "Svoboda", "Dvorak", "Prochazka"),
        ("Obchod", "Lekarna", "Kavarna"),
        ("Lidl", "Albert", "Alza"),
    ),
    "Eurozone": Locale(
        ("Hans", "Anna", "Pierre", "Marie", "Luca"),
        ("Mueller", "Schmidt", "Dupont", "Rossi"),
        ("Markt", "Apotheke", "Cafe"),
        ("Rewe", "Carrefour", "Lidl"),
    ),
    "Mozambique": Locale(
        ("Joao", "Maria", "Carlos", "Ana", "Pedro"),
        ("Santos", "Ferreira", "Costa", "Machel"),
        ("Loja", "Farmacia", "Cafe"),
        ("MCel", "Shoprite", "Vodacom MZ"),
    ),
}

AMOUNT_RANGE: dict[str, tuple[float, float]] = {
    "INR": (20, 80_000),
    "USD": (4, 2_400),
    "AED": (8, 7_000),
    "SAR": (10, 6_000),
    "ETB": (80, 60_000),
    "TZS": (2_000, 1_500_000),
    "NGN": (400, 400_000),
    "NPR": (100, 70_000),
    "EGP": (40, 18_000),
    "KES": (40, 70_000),
    "BDT": (50, 25_000),
    "OMR": (1.5, 350),
    "PKR": (200, 180_000),
    "LKR": (200, 90_000),
    "TRY": (40, 25_000),
    "RUB": (200, 80_000),
    "CZK": (80, 25_000),
    "EUR": (5, 2_500),
    "MZN": (40, 15_000),
}

PREFIXES = ("AD", "AX", "BT", "BV", "JK", "JX", "TX", "VM", "BZ")

TEMPLATES: tuple[Template, ...] = (
    Template("ind_sent", "Indian Bank", "India", "INR", "INDBNK-S", "debit",
             "Sent Rs.{amount} from A/c *{last4} on {date_dmy} to {merchant}."
             "RRN {rrn}.Avl Bal Rs.{balance}.Not you?SMS BLOCK to 9444412345-Indian Bank",
             ("amount", "last4", "merchant", "reference", "balance")),
    Template("ind_debited", "Indian Bank", "India", "INR", "INDBNK-S", "debit",
             "A/c *{last4} debited Rs.{amount} on {date_dmy} to {merchant}."
             "RRN {rrn}. Bal: Rs.{balance}-Indian Bank",
             ("amount", "last4", "merchant", "reference", "balance")),
    Template("ind_credited", "Indian Bank", "India", "INR", "INDBNK-S", "credit",
             "Rs.{amount} credited to A/c *{last4} on {date_dmy} from {merchant}."
             "UPI:{rrn}.Available Balance: Rs.{balance}-Indian Bank",
             ("amount", "last4", "merchant", "reference", "balance")),
    Template("sbi_debit", "State Bank of India", "India", "INR", "SBIBK-S", "debit",
             "Dear SBI User, your A/c XX{last4} has been debited by {amount} on {date_dmy} "
             "trf to {merchant} Ref {rrn}. Avl Bal Rs.{balance}-SBI",
             ("amount", "last4", "merchant", "balance")),
    Template("sbi_credit", "State Bank of India", "India", "INR", "SBIBK-S", "credit",
             "Rs.{amount} has been credited to A/c XX{last4} on {date_dmy} "
             "transfer from {merchant} Ref {rrn}. Avl Bal Rs.{balance}-SBI",
             ("amount", "last4", "merchant", "balance")),
    Template("sbi_spent", "State Bank of India", "India", "INR", "SBIBK-S", "debit",
             "Rs.{amount} spent on card ending {last4} at {merchant} on {date_dmy}. "
             "Your available limit is Rs.{balance}-SBI",
             ("amount", "last4", "merchant", "balance")),
    Template("axis_spent", "Axis Bank", "India", "INR", "AXISBK-S", "debit",
             "Spent INR {amount}\nAxis Bank Card no. XX{last4}\n"
             "{date_dmy} {time} IST\n{merchant}\nAvl Limit: INR {balance}\n"
             "Not you? SMS BLOCK {last4} to 56161510",
             ("last4", "merchant", "balance")),
    Template("axis_upi_debit", "Axis Bank", "India", "INR", "AXISBK-S", "debit",
             "INR {amount} debited from A/c no. XX{last4} on {date_dmy}. "
             "UPI/P2M/{rrn}/{merchant} Not you? SMS BLOCK to 56161510",
             ("amount", "last4", "merchant", "reference")),
    Template("axis_credit", "Axis Bank", "India", "INR", "AXISBK-S", "credit",
             "INR {amount} credited to A/c no. XX{last4} on {date_dmy}. "
             "Info - {merchant}. Chk SMS. Avl Lmt INR {balance}",
             ("amount", "last4")),
    Template("icici_debit", "ICICI Bank", "India", "INR", "ICICIB-S", "debit",
             "Acct XX{last4} is debited with Rs.{amount} on {date_mon} at {merchant}. "
             "Avl Bal Rs.{balance}. UPI:{rrn}-ICICI Bank",
             ("amount", "last4", "balance", "reference")),
    Template("icici_credit", "ICICI Bank", "India", "INR", "ICICIB-S", "credit",
             "Acct XX{last4} is credited with Rs.{amount} on {date_mon} from {merchant}. "
             "Available Balance is Rs.{balance}. UPI:{rrn}-ICICI Bank",
             ("amount", "last4", "balance", "reference")),
    Template("icici_spent", "ICICI Bank", "India", "INR", "ICICIB-S", "debit",
             "INR {amount} spent on ICICI Bank Card XX{last4} on {date_mon} at {merchant}. "
             "Avl Bal Rs.{balance}-ICICI Bank",
             ("amount", "last4", "balance")),
    Template("hdfc_debit", "HDFC Bank", "India", "INR", "HDFCBK-S", "debit",
             "Rs.{amount} debited from HDFC Bank XX{last4} towards {merchant} on {date_mon}. "
             "Avl bal: INR {balance}",
             ("amount", "last4", "merchant", "balance")),
    Template("hdfc_upi", "HDFC Bank", "India", "INR", "HDFCBK-S", "debit",
             "INR {amount} debited from HDFC Bank XX{last4} To {merchant} UPI on {date_dmy4}. "
             "Avl bal: INR {balance}",
             ("amount", "last4", "merchant", "balance")),
    Template("boi_debit", "Bank of India", "India", "INR", "BOIIND-S", "debit",
             "Rs.{amount} debited from A/c XX{last4} towards {merchant} via UPI, "
             "Ref No. {rrn}. Avl Bal: Rs.{balance}-BOI",
             ("amount", "last4", "merchant", "reference", "balance")),
    Template("boi_credit", "Bank of India", "India", "INR", "BOIIND-S", "credit",
             "Rs.{amount} credited to A/c XX{last4} from {merchant} via UPI, "
             "Ref No. {rrn}. Available Balance: Rs.{balance}-BOI",
             ("amount", "last4", "merchant", "reference", "balance")),
    Template("chase_purchase", "Chase", "United States", "USD", "CHASE-S", "debit",
             "Chase: A ${amount} purchase at {merchant} on {date_us} with card ending in {last4}.",
             ("amount", "merchant", "last4")),
    Template("citi_txn", "Citi Bank", "United States", "USD", "CITI-S", "debit",
             "A ${amount} transaction was made at {merchant} on card ending in {last4}.",
             ("amount", "merchant", "last4")),
    Template("discover_txn", "Discover Card", "United States", "USD", "DISCOVER-S", "debit",
             "A transaction of ${amount} at {merchant} on {date_us}.",
             ("amount", "merchant")),
    Template("schwab_debit", "Charles Schwab", "United States", "USD", "SCHWAB-S", "debit",
             "A ${amount} debit card transaction from account ending {last4}.",
             ("amount", "last4")),
    Template("adcb_dr", "Abu Dhabi Commercial Bank", "UAE", "AED", "ADCB-S", "debit",
             "Dr. transaction of AED {amount} in your account XX{last4} at {merchant}, AE. "
             "Avl.Bal AED {balance}",
             ("amount", "last4", "merchant", "balance")),
    Template("enbd_spent", "Emirates NBD", "UAE", "AED", "ENBD-S", "debit",
             "Purchase at {merchant}. Avl Bal AED {balance} card xxxx{last4}",
             ("last4", "merchant", "balance")),
    Template("liv_purchase", "Liv Bank", "UAE", "AED", "LIV-S", "debit",
             "purchase of AED {amount} at {merchant} Avl Balance is AED {balance} "
             "Debit Card ending {last4}",
             ("last4", "merchant", "balance")),
    Template("mashreq_purchase", "Mashreq Bank", "UAE", "AED", "MASHREQ-S", "debit",
             "Purchase for AED {amount} at {merchant} on {date_mash}. "
             "Card ending {last4}. Available Balance is AED {balance}",
             ("last4", "merchant", "balance")),
    Template("rajhi_purchase", "Al Rajhi Bank", "Saudi Arabia", "SAR", "RAJHI-S", "debit",
             "Purchase\nAmount: SAR {amount}\nAt: {merchant}",
             ("amount", "merchant")),
    Template("cbe_debit", "Commercial Bank of Ethiopia", "Ethiopia", "ETB", "CBE-S", "debit",
             "Your account {last4} has been debited for {merchant} with ETB {amount}. "
             "Your Current Balance is ETB {balance}. Ref No {rrn}",
             ("amount", "merchant", "balance", "reference")),
    Template("awash_credit", "Awash Bank", "Ethiopia", "ETB", "AWASH-S", "credit",
             "ETB {amount} has been credited from {merchant} on: {date_slash}. "
             "Balance is ETB {balance} Txn ID: {rrn}",
             ("amount", "balance", "reference")),
    Template("telebirr_pay", "Telebirr", "Ethiopia", "ETB", "TELEBIRR-S", "debit",
             "paid ETB {amount} to {merchant} on {date_slash}. "
             "Your telebirr account balance is ETB {balance} transaction number is {rrn}",
             ("amount", "merchant", "balance", "reference")),
    Template("crdb_paid", "CRDB Bank", "Tanzania", "TZS", "CRDB-S", "debit",
             "Paid: {merchant} TZS {amount} Card: {last4} Balance is TZS {balance}",
             ("amount", "merchant", "last4", "balance")),
    Template("zenith_dr", "Zenith Bank", "Nigeria", "NGN", "ZENITH-S", "debit",
             "Acct:******{last4}\nDR Amt:{amount}\nDesc:{merchant}\nBal:{balance}",
             ("amount", "last4", "balance")),
    Template("access_debit", "Access Bank", "Nigeria", "NGN", "ACCESS-S", "debit",
             "debit\nAmt: NGN {amount}\nAcc: ****{last4}\nDesc: {merchant}\nAvail Bal: NGN {balance}",
             ("amount", "last4", "balance")),
    Template("opay_debit", "Opay", "Nigeria", "NGN", "OPAY-S", "debit",
             "Dear OPay user, N {amount} has been debited for {merchant} on {date_mon}",
             ("amount", "merchant")),
    Template("nabil_debit", "Nabil Bank", "Nepal", "NPR", "NABIL-S", "debit",
             "NPR {amount} debited from A/c #{last4} Remarks: SHOP MTXN{rrn}",
             ("amount", "last4", "reference")),
    Template("nbl_credit", "Nepal Bank Limited", "Nepal", "NPR", "NBL-S", "credit",
             "NPR {amount} credited #{last4} {time}, {merchant}",
             ("amount", "last4", "merchant"), True),
    Template("cib_spent", "CIB Egypt", "Egypt", "EGP", "CIB-S", "debit",
             "Purchase for EGP {amount} at {merchant} on {date_day_mon} with credit card #{last4}. "
             "available limit is EGP {balance}",
             ("amount", "merchant", "last4", "balance")),
    Template("mpesa_paid", "M-PESA", "Kenya", "KES", "MPESA-S", "debit",
             "{rrn10} Confirmed. Ksh{amount} paid to {merchant} 254. on {date_slash}. "
             "New M-PESA balance is Ksh{balance}",
             ("amount", "merchant", "balance", "reference")),
    Template("bkash_pay", "bKash", "Bangladesh", "BDT", "BKASH-S", "debit",
             "Tk {amount} sent. Balance Tk {balance} TrxID {rrn10}",
             ("amount", "balance", "reference")),
    Template("muscat_debit", "Bank Muscat", "Oman", "OMR", "MUSCAT-S", "debit",
             "OMR {amount} debited from your card. رصيدك الحالي هو {balance} OMR",
             ("amount", "balance")),
    Template("faysal_purchase", "Faysal Bank", "Pakistan", "PKR", "FAYSAL-S", "debit",
             "PKR {amount} debit card purchase at {merchant} from FBL A/C ****{last4} Ref {rrn}",
             ("amount", "merchant", "last4", "reference")),
    Template("sampath_debit", "Sampath Bank", "Sri Lanka", "LKR", "SAMPATH-S", "debit",
             "LKR {amount} debited from AC ***{last4} at {merchant} Avl Bal LKR {balance}",
             ("amount", "last4", "merchant", "balance")),
    # extra types on existing banks
    Template("ind_atm", "Indian Bank", "India", "INR", "INDBNK-S", "atm",
             "A/c *{last4} withdrawn Rs.{amount} ATM at {merchant} on {date_dmy}. "
             "Bal: Rs.{balance}-Indian Bank",
             ("amount", "last4", "merchant", "balance")),
    Template("ind_upi_pay", "Indian Bank", "India", "INR", "INDBNK-S", "debit",
             "UPI payment of Rs.{amount} from A/c *{last4} to {merchant}.UPI:{rrn} "
             "Available Balance: Rs.{balance}-Indian Bank",
             ("amount", "last4", "merchant", "reference", "balance")),
    Template("sbi_atm", "State Bank of India", "India", "INR", "SBIBK-S", "atm",
             "ATM withdrawal of Rs.{amount} at {merchant} on {date_dmy} A/c XX{last4}. "
             "Avl Bal Rs.{balance}-SBI",
             ("amount", "last4", "merchant", "balance")),
    Template("sbi_upi", "State Bank of India", "India", "INR", "SBIBK-S", "debit",
             "paid to {upi} Rs.{amount} A/c XX{last4} Avl Bal Rs.{balance}-SBI",
             ("amount", "last4", "balance")),
    Template("hdfc_neft_cr", "HDFC Bank", "India", "INR", "HDFCBK-S", "credit",
             "NEFT Cr-SBIN0001234-{merchant} INR {amount} Avl bal: INR {balance}",
             ("amount", "merchant", "balance")),
    Template("axis_payment", "Axis Bank", "India", "INR", "AXISBK-S", "debit",
             "Payment of INR {amount} from A/c no. XX{last4} on {date_dmy}",
             ("amount", "last4")),
    Template("mpesa_received", "M-PESA", "Kenya", "KES", "MPESA-S", "credit",
             "{rrn10} Confirmed. You have received Ksh{amount} from {merchant} on {date_slash}. "
             "New M-PESA balance is Ksh{balance}",
             ("amount", "merchant", "balance", "reference")),
    Template("adcb_atm", "Abu Dhabi Commercial Bank", "UAE", "AED", "ADCB-S", "atm",
             "AED {amount} withdrawn from acc. XX{last4}. Avl.Bal AED {balance}",
             ("amount", "last4", "balance")),
    Template("schwab_atm", "Charles Schwab", "United States", "USD", "SCHWAB-S", "atm",
             "A ${amount} ATM transaction from account ending {last4}.",
             ("amount", "last4")),
    Template("access_credit", "Access Bank", "Nigeria", "NGN", "ACCESS-S", "credit",
             "credit\nAmt: NGN {amount}\nAcc: ****{last4}\nDesc: {merchant}\nAvail Bal: NGN {balance}",
             ("amount", "last4", "balance")),
    Template("zenith_cr", "Zenith Bank", "Nigeria", "NGN", "ZENITH-S", "credit",
             "Acct:******{last4}\nCR Amt:{amount}\nDesc:{merchant}\nBal:{balance}",
             ("amount", "last4", "balance")),
    # more India banks
    Template("pnb_debit", "Punjab National Bank", "India", "INR", "PNBBNK-S", "debit",
             "A/c XX{last4} debited with Rs.{amount} towards {merchant} for Rs.{amount}. "
             "UPI Ref ID:{rrn} Avl Bal Rs.{balance}",
             ("amount", "last4", "merchant", "reference", "balance")),
    Template("pnb_credit", "Punjab National Bank", "India", "INR", "PNBBNK-S", "credit",
             "Rs.{amount} credited to A/c XX{last4} UPI:{rrn} Avl Bal Rs.{balance}",
             ("amount", "last4", "reference", "balance")),
    Template("bob_spent", "Bank of Baroda", "India", "INR", "BOB-S", "debit",
             "ALERT: INR {amount} is spent on BOBCARD ending {last4}. AvlBal: Rs.{balance} Ref:{rrn}",
             ("amount", "last4", "balance", "reference")),
    Template("bob_credit", "Bank of Baroda", "India", "INR", "BOB-S", "credit",
             "Rs.{amount} Credited to A/c XX{last4} IMPS/{rrn} by {merchant}. AvlBal: Rs.{balance}",
             ("amount", "last4", "merchant", "reference", "balance")),
    Template("federal_spent", "Federal Bank", "India", "INR", "FEDBNK-S", "debit",
             "INR {amount} spent at {merchant} on {date_slash} on your Federal Bank Debit Card {last4}",
             ("amount", "merchant", "last4")),
    Template("federal_received", "Federal Bank", "India", "INR", "FEDBNK-S", "credit",
             "you've received INR {amount} It was sent by {merchant} on {date_dmy} A/c XX{last4}",
             ("amount", "merchant", "last4")),
    Template("idfc_debit", "IDFC First Bank", "India", "INR", "IDFCFB-S", "debit",
             "Debit Rs.{amount} A/C XX{last4} at {merchant} on {date_dmy} New Bal : INR {balance} UPI:{rrn}",
             ("amount", "last4", "merchant", "balance", "reference"), False, True),
    Template("idfc_credit", "IDFC First Bank", "India", "INR", "IDFCFB-S", "credit",
             "A/C XX{last4} credited by Rs.{amount} from {merchant} New balance is INR {balance} IMPS Ref no {rrn}",
             ("amount", "last4", "balance", "reference")),
    Template("indus_debit", "IndusInd Bank", "India", "INR", "INDUSB-S", "debit",
             "INR {amount} debited from IndusInd Account XX{last4} towards {merchant} "
             "Avl BAL of INR {balance} RRN:{rrn}",
             ("amount", "last4", "merchant", "balance", "reference"), True),
    Template("union_debit", "Union Bank of India", "India", "INR", "UNIONB-S", "debit",
             "Rs.{amount} debited from A/C *{last4} to {merchant} on {date_dmy} "
             "ref no {rrn} Avl Bal Rs.{balance}",
             ("amount", "last4", "merchant", "reference", "balance")),
    Template("canara_debit", "Canara Bank", "India", "INR", "CANBNK-S", "debit",
             "INR {amount} has been DEBITED to {merchant}, UPI Ref {rrn} account XX{last4} "
             "Avail.bal INR {balance}-Canara",
             ("amount", "merchant", "reference", "last4", "balance")),
    # US / Gulf / Africa / wallets
    Template("navy_approved", "Navy Federal Credit Union", "United States", "USD", "NFCU-S", "debit",
             "Transaction for ${amount} was approved on debit card {last4} at {merchant} at {time_hm}",
             ("amount", "last4", "merchant")),
    Template("huntington_wd", "Huntington Bank", "United States", "USD", "HUNTINGTON-S", "atm",
             "withdrawal: ${amount} at {merchant}. Acct CK{last4}",
             ("amount", "merchant", "last4")),
    Template("stc_pay", "STC Bank", "Saudi Arabia", "SAR", "STCBANK-S", "debit",
             "Amount: {amount} SAR\nFrom: {merchant}\nVia: {last4}",
             ("amount", "merchant", "last4")),
    Template("ei_purchase", "Emirates Islamic", "UAE", "AED", "EIB-S", "debit",
             "At: {merchant}\nCard Ending: {last4}\nAvailable Balance: AED {balance}",
             ("merchant", "last4", "balance")),
    Template("sabb_ar", "SABB", "Saudi Arabia", "SAR", "SABB-S", "debit",
             "مبلغ: SAR {amount}\nلدى: {merchant}\nبطاقة: ****{last4}\nالرصيد المتاح: SAR {balance}",
             ("amount", "merchant", "last4", "balance")),
    Template("alinma_ar", "Alinma Bank", "Saudi Arabia", "SAR", "ALINMA-S", "debit",
             "بمبلغ: {amount} SAR\nلدى: {merchant}\nحساب: ****{last4}\nالرصيد: {balance} SAR",
             ("amount", "merchant", "last4", "balance")),
    Template("moniepoint_dr", "Moniepoint", "Nigeria", "NGN", "MONIE-S", "debit",
             "Debit Alert\nAmt: NGN {amount}\nAcc: {last4}\nDesc: {merchant}\nBal: NGN {balance}",
             ("amount", "last4", "balance")),
    Template("keystone_dr", "Keystone Bank", "Nigeria", "NGN", "KEYSTN-S", "debit",
             "debit!\nAmt: NGN {amount}\nAcct: ****{last4}\nDesc: {merchant}\nBal: NGN {balance}",
             ("amount", "last4", "balance")),
    Template("jaiz_dr", "Jaiz Bank", "Nigeria", "NGN", "JAIZBK-S", "debit",
             "Amt: N {amount} DR\nAcct: ****{last4}\nDesc: {merchant}\nBal: N {balance}",
             ("amount", "last4", "balance")),
    Template("everest_dr", "Everest Bank", "Nepal", "NPR", "EVEREST-S", "debit",
             "A/c XX{last4} debited by NPR {amount} For: {merchant}. {rrn}",
             ("amount", "last4", "merchant", "reference")),
    Template("nmb_np", "NMB Bank", "Nepal", "NPR", "NMBNP-S", "debit",
             "NPR {amount} at {merchant} on {date_dmy} A/C {last4} Ref: {rrn}",
             ("amount", "merchant", "last4", "reference")),
    Template("arab_egp", "Arab Bank", "Egypt", "EGP", "ARABBK-S", "debit",
             "Purchase from {merchant} for EGP {amount} Card {last4}. Available balance is EGP {balance}",
             ("amount", "merchant", "last4", "balance")),
    Template("tigo_sent", "Tigo Pesa", "Tanzania", "TZS", "TIGOPESA-S", "debit",
             "You have sent TSh {amount} to 255700 - {merchant}. New balance is TSh {balance} TxnId: {rrn}",
             ("amount", "merchant", "balance", "reference")),
    Template("tigo_recv", "Tigo Pesa", "Tanzania", "TZS", "TIGOPESA-S", "credit",
             "You have received TSh {amount} from {merchant}. New balance is TSh {balance} TxnId: {rrn}",
             ("amount", "balance", "reference")),
    Template("dashen_cr", "Dashen Bank", "Ethiopia", "ETB", "DASHEN-S", "credit",
             "ETB {amount} credited from {merchant} on on {date_slash}. "
             "Your current balance is ETB {balance} Ref No:{rrn}",
             ("amount", "balance", "reference"), False, True),
    Template("zemen_pos", "Zemen Bank", "Ethiopia", "ETB", "ZEMENBANK-S", "debit",
             "pos purchase transaction at {merchant} on {date_dmon4} ETB {amount}. "
             "Your Current Balance is ETB {balance} with reference {rrn}",
             ("amount", "merchant", "balance", "reference")),
    Template("enpara_spend", "Enpara", "Turkey", "TRY", "ENPARA-S", "debit",
             "{amount} TL tutarında harcama yapıldı tarihinde 12 - {merchant} firmasında "
             "bağlı {last4} ile biten Encard",
             ("amount", "merchant", "last4")),
    Template("tbank_spend", "T-Bank", "Russia", "RUB", "TBANK-S", "debit",
             "{amount} ₽. {merchant}. Доступно {balance} ₽ *{last4}",
             ("amount", "merchant", "balance", "last4")),
    Template("mbank_cz", "mBank CZ", "Czech Republic", "CZK", "MBANK-S", "debit",
             "{amount} CZK v obchodě {merchant}.",
             ("amount", "merchant")),
    Template("sparkasse_eur", "Sparkasse Rhein-Maas", "Eurozone", "EUR", "SPARKASSE-S", "debit",
             "{amount} EUR Neuer Saldo: {balance} EUR Konto ***{last4}",
             ("amount", "balance", "last4")),
    Template("bpce_eur", "BPCE", "Eurozone", "EUR", "BPCE-S", "debit",
             "debit de {amount} EUR vers {merchant}",
             ("amount", "merchant")),
    Template("mpesa_moz", "M-Pesa Mozambique", "Mozambique", "MZN", "MPESAMZ-S", "debit",
             "Confirmado {rrn10} Transferiste {amount} MT para 84X - {merchant} aos {date_slash}. "
             "novo saldo M-Pesa e de {balance} MT",
             ("amount", "merchant", "balance", "reference")),
    Template("ndb_debit", "National Development Bank", "Sri Lanka", "LKR", "NDBSL-S", "debit",
             "LKR {amount} debited at {merchant}. Avl Bal {balance} AC XXXX{last4}",
             ("amount", "merchant", "balance", "last4")),
    Template("ntb_card", "Nations Trust Bank", "Sri Lanka", "LKR", "NTBSL-S", "debit",
             "for LKR {amount} at {merchant} Available Bal LKR {balance} Card 1234**{last4}",
             ("amount", "merchant", "balance", "last4")),
)

_keys = [t.key for t in TEMPLATES]
if len(_keys) != len(set(_keys)):
    raise RuntimeError("duplicate template keys")
