import { Text, Box, TextArea, Flex } from "@radix-ui/themes";
import { sand } from "@radix-ui/colors";
import { useRef } from "react";
import { PrimaryButton, SecondaryButton } from "./Buttons";
import { CameraIcon } from "@radix-ui/react-icons";
export default function ItineraryInput() {
  const fileInputRef = useRef(null);
  function handleButtonClick() {
    fileInputRef.current.click();
  }
  return (
    <form>
      <Text as="label" htmlFor="Inspiration Image">
        Inspiration Image
      </Text>
      <Flex
        justify={"center"}
        align={"center"}
        gap={"4"}
        style={{ backgroundColor: sand.sand3 }}
        p={"4"}
        direction={"column"}
      >
        <div className="icon-container--large">
          <CameraIcon
            style={{
              width: "100%",
              height: "100%",
              color: sand.sand10,
            }}
            className="icon"
          />
        </div>
        <Text size={"2"}>Upload an image that inspires your trip</Text>
        <SecondaryButton onClick={handleButtonClick}>
          Choose Image
        </SecondaryButton>
        <input
          ref={fileInputRef}
          type="file"
          id="Inspiration Image"
          name="Inspiration Image"
        />
      </Flex>
      <Text as="label" htmlFor="Additional Notes">
        Additional Notes
      </Text>
      <TextArea
        id="Additional Notes"
        name="Additional Notes"
        placeholder="Any additional details or preferences (e.g budget, travel duration...)"
      />
      <PrimaryButton type="submit">Generate Itinerary</PrimaryButton>
    </form>
  );
}
