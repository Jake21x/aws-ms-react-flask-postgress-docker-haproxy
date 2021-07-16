import Document, { Html, Head, Main, NextScript } from 'next/document';

class MyDocument extends Document {
  render() {
    return (
      <Html>
        <Head>
          <link rel="apple-touch-icon" href="/logo.png" />
          <link rel="manifest" href="/manifest.json" />
          <meta name="theme-color" content="#d93131" />
          <meta name="apple-mobile-web-app-status-bar" content="#d93131" />
          <meta
            name="description"
            content="Making our church smart,organize in recording,tracking & monitoring services & activities!"
          />
          <meta name="apple-mobile-web-app-capable" content="yes" />
          <meta name="apple-mobile-web-app-title" content="Church DMS" />
          <meta name="format-detection" content="telephone=no" />
          <meta name="msapplication-tap-highlight" content="no" />
          <meta content="default-src 'self' https://fonts.googleapis.com/ ; style-src 'self'"/> 
          <link
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
            rel="stylesheet"
          />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}

export default MyDocument;
