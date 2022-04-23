import {
  Box,
  Container,
  Grid,
  GridItem,
  useColorModeValue,
} from "@chakra-ui/react";
import MentalHealthScoreCard from "./components/MentalHealthScoreCard";

function App() {
  return (
    <div className="App">
      <Box
        bg={useColorModeValue("gray.100", "gray.900")}
        py="20"
        minH="100vh"
        px={4}
      >
        <Container maxW="container.xl">
          <Grid
            templateRows="repeat(2, 1fr)"
            templateColumns="repeat(5, 1fr)"
            gap={4}
          >
            <GridItem colSpan={5}>
              <MentalHealthScoreCard />
            </GridItem>
            <GridItem colSpan={2} bg="papayawhip" />
            <GridItem colSpan={4} bg="tomato" />
          </Grid>
        </Container>
      </Box>
    </div>
  );
}

export default App;
