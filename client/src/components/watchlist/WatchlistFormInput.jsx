import { Text, Box, TextField } from "@radix-ui/themes";
import { useState } from "react";
import { PrimaryButton } from "../common/Buttons";
import StockSearch from "./StockSearch";
export default function WatchlistFormInput({ uid }) {
  async function handleSubmit(e) {
    e.preventDefault();
  }
  const [watchlistData, setWatchlistData] = useState({
    name: "",
    uid: uid,
    equities: [],
  });
  const [searchInput, setSearchInput] = useState("");
  const handleInputChange = (e) => {
    if (e.target.name === "watchlist-name") {
      setWatchlistData({ ...watchlistData, name: e.target.value });
    }
  };

  const handleSearch = (e) => {
    setSearchInput(e.target.value);
  };

  return (
    <form onSubmit={handleSubmit}>
      <Box>
        <Text as="label" htmlFor="watchlist-name">
          Watchlist Name
        </Text>
        <TextField.Root placeholder="My Watchlist">
          <TextField.Slot
            type="text"
            id="watchlist-name"
            name="watchlist-name"
            value={watchlistData.name}
            onChange={handleInputChange}
            required
          />
        </TextField.Root>
        <StockSearch
          stockSymbol={searchInput}
          stockSearchHandler={handleSearch}
        />
      </Box>
      <PrimaryButton type="submit">Create Watchlist</PrimaryButton>
    </form>
  );
}
