import { Box, Flex, Heading } from "@radix-ui/themes";
import NewWatchlistForm from "./NewWatchlistForm";
import { useState } from "react";
import { PrimaryButton } from "../common/Buttons";
import { useOutletContext } from "react-router";
export default function Watchlist() {
  const [activeForm, setActiveForm] = useState(null);
  const { authenticatedUser } = useOutletContext();
  function openWatchListForm() {
    setActiveForm(0);
  }
  return (
    <Box>
      <Heading>Watchlist</Heading>
      <Flex justify={"between"} align={"center"}>
        <PrimaryButton onClick={openWatchListForm}>
          + Create Watchlist
        </PrimaryButton>
      </Flex>
      {activeForm === 0 && <NewWatchlistForm uid={authenticatedUser.uid} />}
    </Box>
  );
}
