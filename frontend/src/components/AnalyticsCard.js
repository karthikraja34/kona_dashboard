import {
  Box,
  Flex,
  Heading,
  Text,
  Select,
  Skeleton,
  Spinner,
} from "@chakra-ui/react";
import React, { useState } from "react";
import useFetch from "../hooks/useFetch";
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  AreaChart,
  ResponsiveContainer,
  ReferenceLine,
  Area,
  Legend,
  Line,
} from "recharts";

function AnalyticsCard() {
  const [category, setCategory] = useState("1");
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const { response, loading, error } = useFetch(
    `http://localhost:8000/api/v1/score_analytics/?category=${category}&start_date=${startDate}&end_date=${endDate}`
  );

  const updateTimePeriod = (specifier) => {
    const date = new Date();
    let firstDay, lastDay;

    if (specifier == "this_month") {
      firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
      lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
    } else {
      firstDay = new Date(date.getFullYear(), date.getMonth() - 1, 1);
      lastDay = new Date(date.getFullYear(), date.getMonth(), 0);
    }
    setStartDate(firstDay.toISOString().split("T")[0]);
    setEndDate(lastDay.toISOString().split("T")[0]);
  };

  return (
    <>
      <Box
        bg="white"
        minH={350}
        px={8}
        py={6}
        borderWidth="1px"
        borderRadius="lg"
        overflow="hidden"
      >
        <Flex justifyContent={"space-between"} alignItems="center">
          <Heading as="h4" size="md">
            Burnout Analytics
          </Heading>
          <Box display="flex">
            <Select
              placeholder="Select month"
              defaultValue="this_month"
              onChange={(e) => updateTimePeriod(e.target.value)}
            >
              <option value="this_month">This month</option>
              <option value="last_month">Last month</option>
            </Select>

            <Select
              marginLeft={4}
              defaultValue="1"
              onChange={(e) => setCategory(e.target.value)}
            >
              <option value="1">Daywise</option>
              <option value="2">Weekwise</option>
            </Select>
          </Box>
        </Flex>
        <Text color="gray.500" fontWeight="semibold" marginTop={1}>
          Less is better
        </Text>

        <Flex marginTop={6} justifyContent="center">
          {loading && (
            <Spinner
              thickness="4px"
              speed="0.65s"
              marginY={10}
              emptyColor="gray.200"
              color="blue.500"
              size="xl"
            />
          )}
          {response && !loading && (
            <ResponsiveContainer width="100%" height={200}>
              <AreaChart data={response.results}>
                <XAxis dataKey="date_from" />
                <YAxis />
                <CartesianGrid strokeDasharray="3 3" />
                <Tooltip />
                <ReferenceLine
                  y={100}
                  label="Max"
                  stroke="red"
                  strokeDasharray="3 3"
                />
                <Area
                  type="monotone"
                  dataKey="score"
                  name="Burnout percentage"
                  stroke="#8884d8"
                  fill="#8884d8"
                />
                <Legend verticalAlign="top" height={36} />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </Flex>
      </Box>
    </>
  );
}

export default AnalyticsCard;
