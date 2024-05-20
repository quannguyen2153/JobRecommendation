import React from 'react';

const page = () => {
  const url =
    'https://public.tableau.com/views/bootcamp_17161932669370/JobInsights?:showVizHome=no&:embed=true';
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
      }}
    >
      <iframe title="Tableau Dashboard" width="80%" height="100%" src={url} />
    </div>
  );
};

export default page;
