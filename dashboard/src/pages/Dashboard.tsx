import { Text } from "@chakra-ui/react";
import { useEffect } from "react";

function Dashboard() {
  useEffect(() => {
    document.title = "Dashboard";
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <Text>MNC GMAC</Text>
      </header>
    </div>
  );
}

export default Dashboard;
