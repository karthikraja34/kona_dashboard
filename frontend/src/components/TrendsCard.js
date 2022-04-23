import {
  Box,
  Flex,
  Heading,
  Text,
  Avatar,
  Stack,
  Tooltip,
  SkeletonCircle,
  Skeleton,
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
        borderWidth="1px"
        borderRadius="lg"
        overflow="hidden"
      >
        <Flex justifyContent={"space-between"} alignItems="center">
          <Heading as="h4" size="md">
            Trends
          </Heading>
        </Flex>
        <Text color="gray.500" fontWeight="semibold" marginTop={1}>
          These employees had burnout for past 3 days. Hover on their name or
          avatar to see their last checkin.
        </Text>

        <Skeleton isLoaded={!loading}>
          <Flex marginTop={6}>
            <Stack direction="row" overflowX={"scroll"}>
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
        </Skeleton>
      </Box>
    </>
  );
}

export default TrendsCard;
