import { AssetSvg } from '@/assets/AssetSvg';
import { Pagination, Select, SelectItem } from '@nextui-org/react';
import React from 'react';
import JobListItem from './JobListItem';
import JobDescriptionCard from './JobDescriptionCard';

const JobList = ({
  jobData,
  filterOptions,
  setFilter,
  showJobDescriptionModal,
  selectedJob,
  setShowJobDescriptionModal,
  setSelectedJob,
  totalPage,
  currentPage,
  onPageChange,
}: {
  jobData: any;
  filterOptions: any;
  setFilter: any;
  showJobDescriptionModal: boolean;
  selectedJob: any;
  setShowJobDescriptionModal: any;
  setSelectedJob: any;
  totalPage: number | null;
  currentPage: number;
  onPageChange: any;
}) => {
  return (
    <div className="flex flex-col z-10">
      <div className="w-full h-fit flex flex-row justify-between items-center">
        <p className="font-bold text-lg text-black">{jobData?.total} Jobs</p>
        <Select
          className="w-fit"
          style={{ width: '15rem', zIndex: 0 }}
          key={'type'}
          radius={'md'}
          size="lg"
          color="primary"
          autoFocus={false}
          startContent={AssetSvg.filter()}
          placeholder={'Filter by'}
          onSelectionChange={setFilter}
          aria-label="Filter"
        >
          {filterOptions?.map((c) => (
            <SelectItem
              key={c.id}
              value={c.option}
              className="text-black"
              onMouseEnter={() => {}}
            >
              {c.option}
            </SelectItem>
          ))}
        </Select>
      </div>
      <div className="w-full flex flex-col justify-center items-center">
        {
          <div className="w-full h-fit z-0">
            {Array.isArray(jobData?.data) &&
              jobData?.data.map((item, index) => (
                <div
                  key={item.job_url}
                  className={`w-full h-fit flex flex-row items-center justify-between my-2 relative ${
                    showJobDescriptionModal &&
                    selectedJob?.job_url === item.job_url
                      ? 'z-20'
                      : 'z-0'
                  }`}
                  // onClick={() => onJobClick(item)}
                  onMouseEnter={() => {
                    setShowJobDescriptionModal(true);
                    setSelectedJob(item);
                  }}
                  onMouseLeave={() => {
                    setShowJobDescriptionModal(false);
                  }}
                  onClick={() => {
                    setSelectedJob(item);
                  }}
                >
                  <JobListItem
                    data={item}
                    isSelected={selectedJob?.job_url === item.job_url}
                  />{' '}
                  {showJobDescriptionModal &&
                    selectedJob?.job_url === item.job_url && (
                      <div
                        className={`z-10 absolute ${
                          index >= 3
                            ? '-top-72'
                            : index >= 2
                            ? '-top-48'
                            : '-top-16'
                        } right-0 w-1/5`}
                      >
                        <JobDescriptionCard data={item} />
                      </div>
                    )}
                </div>
              ))}
          </div>
        }
        <Pagination
          color="primary"
          showControls
          total={totalPage!}
          initialPage={1}
          onChange={(page) => {
            onPageChange(page);
          }}
          page={currentPage}
        />
      </div>
    </div>
  );
};

export default JobList;
