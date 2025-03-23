import { Box, Flex, Heading } from "@radix-ui/themes";
import NewWatchlistForm from "./NewWatchlistForm";
import { useState } from "react";
import { PrimaryButton, CloseButton } from "../common/Buttons";
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
      <NewWatchlistForm
        uid={authenticatedUser.uid}
        formOpen={activeForm === 0}
        dialogCloseButton={
          <CloseButton
            onClick={() => setActiveForm(null)}
            iconProps={{ width: 20, height: 20 }}
          />
        }
      />
    </Box>
  );
}
