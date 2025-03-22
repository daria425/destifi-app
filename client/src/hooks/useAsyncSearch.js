import { useState, useEffect } from "react";
import { apiConfig } from "../config/api.config";

function useAsyncSearch({ urlPath, searchValue, queryParams }) {
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (searchValue === "") {
      return;
    }
    setLoading(true);
    setError(null);

    const fetchData = async () => {
      try {
        const response = await apiConfig.get(
          `${urlPath}/search?${queryParams}=${searchValue}`
        );
        const data = JSON.parse(response.data);
        setOptions(data); // assuming the data is returned as an array
      } catch (err) {
        setError("Failed to fetch data", err?.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [searchValue, urlPath, queryParams]);
  return { options, loading, error };
}

export { useAsyncSearch };
