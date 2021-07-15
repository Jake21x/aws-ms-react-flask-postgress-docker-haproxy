module.exports = {
  async rewrites() {
    return [
      {
        source: "/api/:slug*",
        destination: "http://13.228.23.99:8981/api/:slug*",
      },
    ];
  },
  reactStrictMode: true,
};
