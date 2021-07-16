module.exports = {
  async rewrites() {
    return [
      {
        source: "/api/:slug*",
        destination: "http://localhost:8981/api/:slug*",
      },
    ];
  },
  reactStrictMode: true,
};
