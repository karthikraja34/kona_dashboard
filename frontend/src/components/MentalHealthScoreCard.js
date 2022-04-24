import React, { useState } from "react";
import {
  Box,
  Flex,
  Heading,
  Select,
  Stack,
  Avatar,
  Text,
  CircularProgress,
  CircularProgressLabel,
} from "@chakra-ui/react";
import useFetch from "../hooks/useFetch";
import EmptyIcon from "../assets/bored.png";

function MentalHealthScoreCard() {
  const [timeline, setTimeline] = useState("today");
  const [team, setTeam] = useState(null);
  const { response } = useFetch("http://localhost:8000/api/v1/teams/");
  const getURL = () => {
    let url = `http://localhost:8000/api/v1/scores/?timeline=${timeline}`;
    if (team) {
      url = `${url}&team=${team}`;
    }
    return url;
  };
  const {
    response: scoresResponse,
    loading,
    error,
    refetch,
  } = useFetch(getURL());

  const getBorderColor = (score) => {
    if (score > 70) {
      return "green.500";
    } else if (score > 40) {
      return "yellow.500";
    }

    return "red.600";
  };

  return (
    <div>
      <Box
        bg="white"
        px={8}
        py={6}
        borderWidth="1px"
        borderRadius="lg"
        overflow="hidden"
      >
        <Flex justifyContent={"space-between"} alignItems="center">
          <Heading as="h4" size="md">
            Mental Health Scorecard
          </Heading>
          <Box display="flex">
            <Select
              placeholder="Select team"
              defaultValue=""
              onChange={(e) => setTeam(e.target.value)}
            >
              <option value="">All</option>
              {response &&
                response.results.map((team) => (
                  <option key={team.id} value={team.id}>
                    {team.name}
                  </option>
                ))}
            </Select>

            <Select
              marginLeft={4}
              defaultValue="today"
              onChange={(e) => setTimeline(e.target.value)}
            >
              <option value="today">Today</option>
              <option value="this_week">This Week</option>
              <option value="this_month">This Month</option>
            </Select>
          </Box>
        </Flex>

        <Flex marginTop={10}>
          {scoresResponse && !scoresResponse.results.length && (
            <Box
              w="full"
              alignItems="center"
              flexDirection="column"
              display="flex"
              marginBottom={10}
            >
              <img src={EmptyIcon} alt="No data" />
              <Text color="gray.500" fontWeight="semibold" fontSize="xl">
                Seems no checkins yet available!!!
              </Text>
            </Box>
          )}
          <Stack direction="row" overflowX={"scroll"}>
            {scoresResponse &&
              scoresResponse.results.map((scoreData) => (
                <Box textAlign="center" padding={4}>
                  <CircularProgress
                    color={getBorderColor(scoreData.score)}
                    size="120px"
                    value={scoreData.score}
                  >
                    <CircularProgressLabel>
                      <Avatar size="xl" name={scoreData.user.username} />
                    </CircularProgressLabel>
                  </CircularProgress>
                  <h4 className="text-gray-500 font-semibold text-sm mt-2">
                    {scoreData.user.username}
                  </h4>
                  <h5 className="text-gray-900 font-bold text-sm">
                    {scoreData.score}
                  </h5>
                </Box>
              ))}
          </Stack>
        </Flex>
      </Box>
    </div>
  );
}

export default MentalHealthScoreCard;
