import { useState, useEffect, useCallback } from "react";
import { apiConfig } from "../config/api.config";

function useAsyncSearch({ urlPath, searchValue, queryParams, delay = 1000 }) {
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    if (searchValue === "") {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      console.log("Executing API call");
      const response = await apiConfig.get(
        `${urlPath}/search?${queryParams}=${searchValue}`
      );
      const data = JSON.parse(response.data);
      setOptions(data);
    } catch (err) {
      setError("Failed to fetch data", err?.message);
    } finally {
      setLoading(false);
    }
  }, [searchValue, urlPath, queryParams]);

  useEffect(() => {
    if (searchValue === "") {
      setOptions([]);
      return;
    }

    // Set a timer that will execute after the specified delay
    const timerId = setTimeout(() => {
      fetchData();
    }, delay);

    // Clear the timer if searchValue changes before the delay completes
    return () => clearTimeout(timerId);
  }, [searchValue, fetchData, delay]);

  return { options, loading, error };
}

export { useAsyncSearch };
