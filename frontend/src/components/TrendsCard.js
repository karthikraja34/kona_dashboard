import {
  Box,
  Flex,
  Heading,
  Text,
  Avatar,
  Stack,
  Tooltip,
  Skeleton,
  Spinner,
} from "@chakra-ui/react";
import React from "react";
import useFetch from "../hooks/useFetch";

function TrendsCard() {
  const { response, loading, error } = useFetch(
    "http://localhost:8000/api/v1/trends/"
  );

  return (
    <>
      <Box
        bg="white"
        px={8}
        py={6}
        minH={350}
        borderWidth="1px"
        borderRadius="lg"
        overflow="hidden"
      >
        <Flex justifyContent={"space-between"} alignItems="center">
          <Heading as="h4" size="md">
            Trends
          </Heading>
        </Flex>
        {response && response.results && (
          <Text color="gray.500" fontWeight="semibold" marginTop={1}>
            These employees had burnout for past 3 days. Hover on their name or
            avatar to see their last checkin.
          </Text>
        )}

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
          <Stack direction="row" overflowX={"scroll"}>
            {response && !response.results.length && (
              <>
                <Box
                  w="full"
                  alignItems="center"
                  flexDirection="row"
                  display="flex"
                  marginBottom={10}
                >
                  <Text color="gray.500" fontWeight="semibold" fontSize="xl">
                    Hey there!! More trends yet to come soon
                  </Text>
                </Box>
              </>
            )}
            {response &&
              response.results.map((checkin) => (
                <Box textAlign="center" padding={4}>
                  <Tooltip
                    label={
                      checkin.elaboration ? checkin.elaboration : "No data"
                    }
                  >
                    <Avatar size="xl" name={checkin.user.username} />
                  </Tooltip>
                  <Tooltip
                    label={
                      checkin.elaboration ? checkin.elaboration : "No data"
                    }
                  >
                    <h4 className="text-gray-500 font-semibold text-sm mt-2">
                      {checkin.user.username}
                    </h4>
                  </Tooltip>
                </Box>
              ))}
          </Stack>
        </Flex>
      </Box>
    </>
  );
}

export default TrendsCard;
