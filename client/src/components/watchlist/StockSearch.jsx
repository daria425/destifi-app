import AsyncSearchableSelect from "../common/AsyncSearchableSelect";

export default function StockSearch({ stockSymbol, stockSearchHandler }) {
  return (
    <AsyncSearchableSelect
      urlPath={"/equities"}
      searchHandler={stockSearchHandler}
      searchValue={stockSymbol}
      queryParams={"ticker"}
    />
  );
}
