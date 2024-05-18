import { Button, Select, SelectItem } from '@nextui-org/react';
import React, { useEffect, useState } from 'react';

const Filter = ({ data, isOpen }) => {
  const [major, setMajor] = useState(new Set([]));
  const [location, setLocation] = useState(new Set([]));
  const [salaryRange, setSalaryRange] = useState(new Set([]));
  const majors = [
    { id: 1, major: 'MajorA' },
    { id: 2, major: 'MajorB' },
  ];
  const locations = [
    { id: 1, location: 'HCM' },
    { id: 2, location: 'HN' },
    { id: 3, location: 'Danang' },
    { id: 4, location: 'Hue' },
  ];
  const salaryRanges = [
    { id: 1, majorId: 1, salaryRange: '0 -> 5tr' },
    { id: 2, majorId: 1, salaryRange: '5 -> 15tr' },
    { id: 3, majorId: 1, salaryRange: '15 -> 30tr' },
    { id: 4, majorId: 1, salaryRange: '> 30tr' },
  ];

  return (
    <div
      className={`${
        !isOpen
          ? `w-fit h-fit flex flex-row border-3
         border-primary rounded-xl p-2 gap-3 text-primary animate-appearance-out duration-500`
          : `w-fit h-fit flex flex-row border-3
         border-primary rounded-xl p-2 gap-3 text-primary`
      }`}
    >
      <div className="w-[15rem] h-fit flex flex-row items-center justify-evenly">
        <Select
          style={{ height: '3rem' }}
          key={'type'}
          radius={'md'}
          size="sm"
          autoFocus={false}
          color={'primary'}
          placeholder={'Major'}
          onSelectionChange={setMajor}
          aria-label="Major filter"
        >
          {majors?.map((c) => (
            <SelectItem key={c.id} value={c.major} className="text-primary">
              {c.major}
            </SelectItem>
          ))}
        </Select>
      </div>
      <div className="w-[15rem] h-fit flex flex-row gap-3 items-center">
        <Select
          style={{ height: '3rem' }}
          size="sm"
          key={'type'}
          radius={'md'}
          autoFocus={false}
          color={'primary'}
          placeholder={'Location'}
          onSelectionChange={setLocation}
          aria-label="Location filter"
        >
          {locations?.map((c) => (
            <SelectItem key={c.id} value={c.location} className="text-primary">
              {c.location}
            </SelectItem>
          ))}
        </Select>
      </div>
      <div className="w-[15rem] h-fit flex flex-row gap-3 items-center">
        <Select
          style={{ height: '3rem' }}
          size="sm"
          key={'type'}
          radius={'md'}
          autoFocus={false}
          color={'primary'}
          placeholder={'Salary range'}
          onSelectionChange={setSalaryRange}
          aria-label="Salary range filter"
        >
          {salaryRanges?.map((c) => (
            <SelectItem
              key={c.id}
              value={c.salaryRange}
              className="text-primary"
            >
              {c.salaryRange}
            </SelectItem>
          ))}
        </Select>
      </div>
    </div>
  );
};

export default Filter;
