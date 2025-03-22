import { useState, useEffect } from "react";
import { apiConfig } from "../config/api.config";

function useAsyncSearch({ urlPath, searchValue }) {
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    const fetchData = async () => {
      try {
        const response = await apiConfig.get(
          `${urlPath}?search=${searchValue}`
        );
        const data = await response.json();
        setOptions(data); // assuming the data is returned as an array
      } catch (err) {
        setError("Failed to fetch data", err?.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [searchValue, urlPath]);
  return { options, loading, error };
}

export { useAsyncSearch };
