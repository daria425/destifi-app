import { Box, Flex, Heading, Text } from "@radix-ui/themes";
import { useState } from "react";
import { PrimaryButton } from "./Buttons";
import { useOutletContext } from "react-router";
import NewItinerary from "./NewItinerary";
export default function Dashboard() {
  const [activeForm, setActiveForm] = useState(null);
  const { authenticatedUser } = useOutletContext();
  function openNewItineraryForm() {
    setActiveForm(0);
  }
  return (
    <Box>
      <Heading>My Itineraries</Heading>
      <Flex justify={"between"} align={"center"}>
        <Text>View and manage your itineraries here</Text>
        <PrimaryButton onClick={openNewItineraryForm}>
          + New Itinerary
        </PrimaryButton>
      </Flex>
      {activeForm === 0 && <NewItinerary uid={authenticatedUser.uid} />}
    </Box>
  );
}
