import { Box, Flex, Heading, Text } from "@radix-ui/themes";
import { useState } from "react";
import { PrimaryButton } from "./Buttons";
import NewItinerary from "./NewItinerary";
export default function Dashboard() {
  const [activeForm, setActiveForm] = useState(null);
  function openNewItineraryForm() {
    console.log(activeForm);
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
      {activeForm === 0 && <NewItinerary />}
    </Box>
  );
}
