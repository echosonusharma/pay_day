from pydantic import BaseModel, ConfigDict


class PennywiseRegex(BaseModel):
    """Single regex entry from pennywiseai-tracker."""

    id: int
    file: str
    line: int
    column: int
    module: str
    type: str
    quoteType: str
    pattern: str
    options: str | None = None
    raw: str
    lineContent: str
    bank: str | None = None
    country: str | None = None
    flag: str | None = None
    currency: str | list[str] | None = None
    symbol: str | list[str] | None = None
    category: str | None = None

    model_config = ConfigDict(extra="ignore")


class PennywiseMeta(BaseModel):
    generated: str
    description: str
    total: int
    totalBanks: int
    totalCountries: int

    model_config = ConfigDict(extra="allow")


class CountryBanks(BaseModel):
    country: str
    flag: str | None = None
    currency: str | None = None
    symbol: str | None = None
    bankCount: int
    banks: list[str]

    model_config = ConfigDict(extra="ignore")


class SupportedBanks(BaseModel):
    totalBanks: int
    totalCountries: int
    countries: list[CountryBanks]

    model_config = ConfigDict(extra="allow")


class PennywiseData(BaseModel):
    """Root object of raw_data/pennywise_regex.json."""

    meta: PennywiseMeta
    regexes: list[PennywiseRegex]
    supportedBanks: SupportedBanks

    model_config = ConfigDict(extra="ignore")
