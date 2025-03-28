import { Box, TextField, Badge, Flex } from "@radix-ui/themes";
import { useState } from "react";
import { PrimaryButton } from "../common/Buttons";
import StockSearch from "./StockSearch";
import InputLabel from "../common/InputLabel";
export default function WatchlistFormInput({ uid }) {
  async function handleSubmit(e, watchlistData) {
    e.preventDefault();
    console.log(watchlistData);
  }
  const [watchlistData, setWatchlistData] = useState({
    uid: uid,
    watchlist: {
      name: "",
      equities: [],
    },
  });
  const [searchInput, setSearchInput] = useState("");
  const [selectDropdownOpen, setSelectDropdownOpen] = useState(true);
  const isAdded = (stock) => {
    return watchlistData.watchlist.equities.some(
      (equity) => equity.symbol === stock.symbol
    );
  };

  const handleInputChange = (e) => {
    if (e.target.name === "watchlist-name") {
      setWatchlistData({
        ...watchlistData,
        watchlist: {
          ...watchlistData.watchlist,
          name: e.target.value,
        },
      });
    }
  };

  const handleSelect = (stock) => {
    if (!isAdded(stock)) {
      setWatchlistData({
        ...watchlistData,
        watchlist: {
          ...watchlistData.watchlist,
          equities: [...watchlistData.watchlist.equities, stock],
        },
      });
    }
    setSearchInput("");
    setSelectDropdownOpen(false);
  };

  const handleSearch = (e) => {
    if (!selectDropdownOpen) {
      setSelectDropdownOpen(true);
    }
    setSearchInput(e.target.value);
  };

  const handleOpenDropdown = () => {
    setSelectDropdownOpen(true);
  };
  const handleCloseSelect = () => {
    setSelectDropdownOpen(false);
  };
  return (
    <form onSubmit={(e) => handleSubmit(e, watchlistData)}>
      <Box>
        <InputLabel labelText="Watchlist Name" inputId="watchlist-name" />
        <TextField.Root
          placeholder="My Watchlist"
          type="text"
          id="watchlist-name"
          name="watchlist-name"
          value={watchlistData.name}
          onChange={handleInputChange}
          onClick={handleCloseSelect}
          required
        ></TextField.Root>
        <StockSearch
          isAdded={isAdded}
          stockSymbol={searchInput}
          stockSearchHandler={handleSearch}
          stockSelectHandler={handleSelect}
          selectDropdownOpen={selectDropdownOpen}
          handleOpenDropdown={handleOpenDropdown}
        />
      </Box>
      {watchlistData.watchlist.equities.length > 0 && (
        <Flex>
          {watchlistData.watchlist.equities.map((equity) => (
            <Badge key={equity.symbol} color="blue">
              {equity.symbol}
            </Badge>
          ))}
        </Flex>
      )}
      <PrimaryButton
        disabled={
          watchlistData.watchlist.equities.length === 0 ||
          watchlistData.watchlist.name.trim() === ""
        }
        type="submit"
      >
        Create Watchlist
      </PrimaryButton>
    </form>
  );
}
