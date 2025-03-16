import { Text, Box, TextArea, Flex } from "@radix-ui/themes";
import { apiConfig } from "../config/api.config";
import { sand } from "@radix-ui/colors";
import { useRef, useState } from "react";
import { useNavigate } from "react-router";
import { PrimaryButton, SecondaryButton } from "./Buttons";
import { CameraIcon } from "@radix-ui/react-icons";
export default function ItineraryInput({ uid }) {
  const nav = useNavigate();
  const fileInputRef = useRef(null);
  const [imageFile, setImageFile] = useState(null);
  function handleButtonClick() {
    fileInputRef.current.click();
  }
  function handleImageFileChange(e) {
    const uploadedImageFile = e.target.files[0];
    if (uploadedImageFile) {
      setImageFile(uploadedImageFile);
    }
  }
  async function handleSubmit(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append("image_file", imageFile);

    try {
      const response = await apiConfig.post("chat/itinerary/create", formData, {
        params: {
          uid,
        },
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.status === 200) {
        const { data } = response.data;
        nav(`/app/chat/${data.thread_id}`, {
          state: { responseData: data },
        });
      }
    } catch (error) {
      console.error("Error creating itinerary:", error);
      // Handle error appropriately
    }
  }

  return (
    <form onSubmit={handleSubmit}>
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
          onChange={handleImageFileChange}
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
