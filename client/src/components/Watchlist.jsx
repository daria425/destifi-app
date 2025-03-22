import { Box, Flex, Heading, Text } from "@radix-ui/themes";
import { useState } from "react";
import { PrimaryButton } from "./Buttons";
import { useOutletContext } from "react-router";
export default function Watchlist() {
  const [activeForm, setActiveForm] = useState(null);
  const { authenticatedUser } = useOutletContext();
  function openNewStockForm() {
    setActiveForm(0);
  }
  return (
    <Box>
      <Heading>Watchlist</Heading>
      <Flex justify={"between"} align={"center"}>
        <PrimaryButton onClick={() => {}}>+ Create Watchlist</PrimaryButton>
      </Flex>
    </Box>
  );
}
