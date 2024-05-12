import type { Metadata } from 'next';
import { Montserrat } from 'next/font/google';
import './globals.css';

const montserrat = Montserrat({
  subsets: ['latin'],
  variable: '--font-mont',
  weight: '500',
});

const metadata: Metadata = {
  title: 'Job Recommender',
  description: 'Help you find the best job for you!',
};

const RootLayout = ({ children }: { children: React.ReactNode }) => {
  //use mock session
  // const session = await getSession();
  const session = {
    user: {
      email: 'abc@gmail.com',
      avatar: '/ic_human.png',
    },
  };

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
