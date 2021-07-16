module.exports = {
  async rewrites() {
    return [
      {
        source: "/api/:slug*",
        destination: "http://34.221.170.139:8981/api/:slug*",
      },
    ];
  },
  reactStrictMode: true,
};
