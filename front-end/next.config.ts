import type { NextConfig } from "next"
import createNextIntlPlugin from 'next-intl/plugin'

const nextConfig: NextConfig = {
    webpack(config) {
        config.module.rules.push({
          test: /\.svg$/,
          use: [
            {
              loader: '@svgr/webpack',
              options: {
                icon: true, 
              },
            },
          ],
        });
    
        return config;
      },
       images: {
        domains: ['i.ibb.co']
       },
       reactStrictMode:false
};

const withNextIntl = createNextIntlPlugin();
export default withNextIntl(nextConfig);
