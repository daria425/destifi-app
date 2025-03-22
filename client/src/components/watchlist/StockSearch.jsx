import AsyncSearchableSelect from "../common/AsyncSearchableSelect";
import InputLabel from "../common/InputLabel";
export default function StockSearch({ stockSymbol, stockSearchHandler }) {
  return (
    <AsyncSearchableSelect
      urlPath={"/equities"}
      searchHandler={stockSearchHandler}
      searchValue={stockSymbol}
      queryParams={"ticker"}
      textFieldProps={{
        placeholder: "Search stocks by ticker",
        name: "stock-search",
        id: "stock-search",
      }}
      searchLabel={<InputLabel labelText="Add Stocks" inputId="stock-search" />}
    />
  );
}
