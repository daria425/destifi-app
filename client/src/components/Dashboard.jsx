import { Box, Flex, Heading, Text } from "@radix-ui/themes";
import PrimaryButton from "./PrimaryButton";
export default function Dashboard() {
  return (
    <Box>
      <Heading>My Itineraries</Heading>
      <Flex justify={"between"} align={"center"}>
        <Text>View and manage your itineraries here</Text>
        <PrimaryButton>+ New Itinerary</PrimaryButton>
      </Flex>
    </Box>
  );
}
