import DialogForm from "./DialogForm";
import ItineraryInput from "./ItineraryInput";
export default function NewItinerary({ uid }) {
  return (
    <DialogForm title="New Itinerary">
      <ItineraryInput uid={uid} />
    </DialogForm>
  );
}
