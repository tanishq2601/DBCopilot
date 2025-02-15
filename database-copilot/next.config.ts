import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/query",
        destination: "http://localhost:8080/databse_copilot",
      },
    ];
  },
};

export default nextConfig;
