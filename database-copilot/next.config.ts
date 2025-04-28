import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/query",
<<<<<<< HEAD
        destination: "http://localhost:8080/databse_copilot",
=======
        destination: "http://localhost:8085/databse_copilot",
>>>>>>> c55302b (final changes to perfect)
      },
    ];
  },
};

export default nextConfig;
