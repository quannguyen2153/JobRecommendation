import type { Metadata } from 'next';
import { Montserrat } from 'next/font/google';
import './globals.css';

const montserrat = Montserrat({
  subsets: ['latin'],
  variable: '--font-mont',
  weight: '500',
});

const metadata: Metadata = {
  title: 'Oppurtuno',
  description: "We'll help find the best job for you!",
};

const RootLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <html lang="en">
      <body
        className={`${montserrat.variable} ${montserrat.style.fontWeight} font-mont`}
      >
        <div className="w-full h-full bg-white">
          {/* <Header session={session} /> */}
          {children}
        </div>
      </body>
    </html>
  );
};

export { metadata };
export default RootLayout;
