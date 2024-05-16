'use client';
import React, { useEffect, useState } from 'react';
import Filter from './Filter';
import {
  Button,
  Input,
  Link,
  Pagination,
  Select,
  SelectItem,
} from '@nextui-org/react';
import { AssetSvg } from '@/assets/AssetSvg';
import JobListItem from './JobListItem';
import JobDescriptionCard from './JobDescriptionCard';
import FileCard from '@/components/FileCard/FileCard';
import { FileDialog } from '@/components/FileDialog';
import ChatInput from './ChatInput';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import { useUser } from '@/hooks/useUser';
import { set } from 'react-hook-form';

const sampleJobData = [
  {
    job_title: 'Nhân Viên Phụ Trách Kênh Bán Hàng Nhà Phân Phối, Đại Lý',
    job_url:
      'https://www.vietnamworks.com/nhan-vien-phu-trach-kenh-ban-hang-nha-phan-phoi-dai-ly-1766882-jv?source=searchResults&searchType=2&placement=1770432&sortBy=latest',
    company_name: 'Công Ty Cổ Phần Máy - Thiết Bị Dầu Khí (PV Machino)',
    company_url:
      'https://www.vietnamworks.com/nha-tuyen-dung/cong-ty-co-phan-may-thiet-bi-dau-khi-pv-machino-c165881?fromPage=jobDetail',
    location: 'Hàng Trống, Hoàn Kiếm, Hà Nội',
    post_date: new Date(1713286800),
    due_date: new Date(1716396706842),
    fields: 'Kinh Doanh > Bán Hàng/Phát Triển Kinh Doanh',
    salary: 'Thương lượng',
    experience: null,
    position: 'Nhân viên',
    benefits: [
      'Thưởng\nLương, thưởng theo quy chế, kết quả kinh doanh của Công ty',
      'Chăm sóc sức khoẻ\nBHXH, BHYTcùng những chế độ khác theo quy định của Nhà nước',
      'Hoạt động nhóm\nMôi trường làm việc năng động, thân thiện, được tạo cơ hội phát triển nghề nghiệp',
    ],
    job_description:
      '* Mô tả công việc.\n- Tìm kiếm khách hàng tại các tỉnh chưa có Nhà phân phối, chăm sóc, hợp tác với nhà phân phối hiện có để phát triển đại lý.\n- Xây dựng kế hoạch kinh doanh với từng Nhà phân phối, triển khai các hoạt động bán hàng, phát triển thị trường nhằm đảm bảo hoàn thành mục tiêu thị trường.\n- Xây dựng, đề xuất chính sách kinh doanh phù hợp với từng thị trường theo giai đoạn phát triển.\n- Hướng dẫn và đưa ra các công cụ bán hàng phù hợp để các đại lý am hiểu sản phẩm và kinh doanh thuận lợi.',
    requirements:
      '* Yêu cầu:\n- Số lượng: 02 người\n- Giới tính: Nam/Nữ, tuổi từ 26-40 tuổi.\n- Trình độ chuyên môn: Tốt nghiệp Cao Đẳng trở lên.\n- Tư duy nhạy bén, yêu thích kinh doanh, có kỷ luật trong công việc, sẵn sàng đi công tác tỉnh.\n- Có kinh nghiệm tại vị trí tương đương, ưu tiên các ứng viên am hiểu về thị trường các ngành điện, điện tử, gia dụng, nội thất, vật liệu xây dựng...\n- Có khả năng làm việc với đối tác một cách hiệu quả, có khả năng mở được nhà phân phối.\n- Có khả năng tuyển dụng và đào tạo nhân sự cấp dưới.\n\n* Chế độ đãi ngộ.\n- Mức thu nhập hấp dẫn theo năng lực và khả năng đóng góp (Lương cơ bản, công tác phí, thưởng doanh thu không hạn chế), chi tiết trao đổi khi phỏng vấn.\n- Đóng bảo hiểm theo Luật Lao động. Nghỉ Lễ, tết theo quy định của Nhà nước.\n* Địa điểm làm việc: Hà Nội.',
  },
  {
    job_title: 'Chuyên Viên Tư Vấn Nước Hoa',
    job_url:
      'https://www.vietnamworks.com/chuyen-vien-tu-van-nuoc-hoa-1766939-jv?source=searchResults&searchType=2&placement=1770489&sortBy=latest',
    company_name: 'Estee Lauder Vietnam',
    company_url:
      'https://www.vietnamworks.com/nha-tuyen-dung/estee-lauder-vietnam-c369009?fromPage=jobDetail',
    location:
      '92-94 Đ. Nam Kỳ Khởi Nghĩa, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh 700000, Việt Nam',
    post_date: new Date(1713286800),
    due_date: new Date(1716396706842),
    fields: 'Dịch Vụ Khách Hàng > Dịch Vụ Khách Hàng',
    salary: 'Thương lượng',
    experience: null,
    position: 'Nhân viên',
    benefits: [
      'Thưởng\nLương tháng 13 và thưởng hiệu quả công việc',
      'Chăm sóc sức khoẻ\nChương trình chăm sóc sức khỏe dành cho nhân viên',
      'Nghỉ phép có lương\n14 ngày phép/năm',
    ],
    job_description:
      '• Cung cấp dịch vụ chăm sóc khách hàng cao cấp, tư vấn sản phẩm phù hợp với nhu cầu khách hàng.\n• Đạt doanh số bán hàng theo ngày và theo tuần cũng như các chỉ tiêu KPI thông qua tư vấn khách hang với kiến thức về thương hiệu JO MALONE LONDON và các dịch vụ chăm sóc khách hàng của JO MALONE LONDON.\n• Thúc đẩy và duy trì hình ảnh thương hiệu JO MALONE LONDON với sứ mệnh và giá trị Dịch vụ JO MALONE LONDON.\n• Xây dựng mối quan hệ lâu dài với khách hàng thông qua Danh sách Đăng ký Khách hàng, các sự kiện đặc biệt, tập trung vào dịch vụ khách hàng và đề xuất sản phẩm theo nhu cầu.\n• Tham gia các hội thảo và buổi hướng dẫn của JO MALONE LONDON để hiểu biết về lịch sử thương hiệu và câu chuyện về sản phẩm.\n• Tham gia vào các buổi huấn luyện về quy trình/tiêu chuẩn phù hợp để xây dựng và duy trì kiến thức và kỹ năng nâng cao.\n• Hỗ trợ duy trì các hoạt động tại cửa hàng.',
    requirements:
      'Bán hàng và cung cấp dịch vụ khách hàng\n• Cung cấp dịch vụ cao cấp và trải nghiệm sang trọng cho mỗi khách hàng theo Hướng dẫn Dịch vụ cao cấp JO MALONE LONDON .\n• Lắng nghe và linh hoạt trong cuộc tư vấn để đáp ứng nhu cầu cá nhân và nhu cầu dưỡng da của từng khách hàng, luôn giữ thái độ tích cực và chỉn chu về ngoại hình.\n• Đề xuất chế độ chăm sóc da phù hợp dựa trên nhu cầu và lối sống của khách hàng.\n• Thể hiện tinh thần của JO MALONE LONDON đến với khách hàng thông qua kiến thức về sản phẩm và kỹ năng bán hàng tuân thủ theo 5 bước của Dịch vụ JO MALONE LONDON .\n• Lắng nghe và hiểu ý kiến phản hồi của khách hàng về sản phẩm và dịch vụ, cung cấp phản hồi cho Cửa hang Trưởng.\n• Theo dõi các thông tin để tương tác với khách hàng, (ví dụ như lời cảm ơn và lời chúc sinh nhật), mẫu thử và các dịch vụ khách hàng khác theo các chương trình Tiếp thị và Danh sách Khách hàng (ví dụ, tư vấn tại cửa hàng, dịch vụ chăm sóc da mặt hoặc sự kiện đặc biệt.)\n• Đề xuất phản hồi và gợi ý về việc cung cấp các cuộc tư vấn Dịch vụ cá nhân độc đáo phù hợp với trải nghiệm thư giãn và trị liệu tại cabine đặc biệt và/hoặc nhu cầu lối sống của mỗi khách hàng.\n\n\nVận hành Cửa hàng, Kiểm kê kho sản phẩm, hỗ trợ tổ chức chương trình Khuyến mãi và Sự kiện Ra mắt\n• Xây dựng và duy trì không gian cabine và trải nghiệm mua sắm sang trọng, thoải mái, dễ chịu và sạch sẽ cho mỗi khách hang.\n• Chỉn chu trong việc trưng bày quầy gọn gàng và bắt mắt với sản phẩm sẵn có\n• Đảm bảo các sản phẩm trưng bày và sản phẩm trải nghiệm sạch sẽ và đầy đủ.\n• Đảm bảo tất cả các trưng bày sản phầm, vật dụng trong phòng được thực hiện theo hướng dẫn JO MALONE LONDON .\n• Đảm bảo nhận thức về tiêu chuẩn trưng bày, các thay đổi và khuyến mãi sản phẩm và duy trì hình ảnh thương hiệu.\n• Trợ giúp Quản lý Quầy theo dõi tồn kho và mức tồn kho.\n• Tổ chức các chương trình khuyến mãi ra mắt và/hoặc sự kiện với khách hàng và hỗ trợ các hoạt động gửi thông tin liên quan đến khách hàng.\n\n\nHỗ trợ quản lý danh sách khách hàng\n• Duy trì hệ thống Danh sách Khách hàng: thêm khách hàng vào hệ thống danh sách và cập nhật thông tin cho mỗi lần khách hang tới cửa hàng.\n• Phát triển và quản lý mối quan hệ với khách hàng và sử dụng danh sách khách hàng để cung cấp dịch vụ cá nhân hóa và xây dựng mối quan hệ lâu dài.\n• Hoàn thành đăng ký danh sách khách hàng, sử dụng các quy trình theo dõi bao gồm việc thêm thông tin khách hàng vào sổ nhật ký cung cấp, liên hệ qua điện thoại hoặc tin nhắn, email cảm ơn, v.v.\n\n\nDuy trì hình ảnh Thương hiệu JO MALONE LONDON : Yêu cầu chăm sóc ngoại hình cá nhân và Hướng dẫn Đồng phục\n• Đảm bảo diện mạo lịch sự, chuyên nghiệp và phản ánh sự tự tin, duyên dáng và chuyên môn về chăm sóc da.\n• Tuân thủ các yêu cầu về chăm sóc ngoại hình và hướng dẫn đồng phục của JO MALONE LONDON và thể hiện sự sang trọng của thương hiệu.',
  },
  {
    job_title: 'Furniture Inspector',
    job_url:
      'https://www.vietnamworks.com/furniture-inspector-1766935-jv?source=searchResults&searchType=2&placement=1770485&sortBy=latest',
    company_name: 'Bureau Veritas Consumer Products Services Vietnam Ltd.',
    company_url:
      'https://www.vietnamworks.com/nha-tuyen-dung/bureau-veritas-consumer-products-services-vietnam-ltd-c97921?fromPage=jobDetail',
    location: 'Ho Chi Minh',
    post_date: new Date(1713286800),
    due_date: new Date(1717519483679),
    fields:
      'Sản Xuất > Đảm Bảo Chất Lượng/Kiểm Soát Chất Lượng/Quản Lý Chất Lượng',
    salary: '$700 - $1000',
    experience: null,
    position: 'Nhân viên',
    benefits: [
      'Thưởng\n13th salary, KPI bonus',
      'Chăm sóc sức khoẻ\nHealth Care Insurance',
      'Máy tính xách tay\nCompany laptop',
    ],
    job_description:
      '- Study both Bureau Veritas & Client’ inspection requirements to ensure full understanding before job execution.\n\n\n- Execute the job(s) assigned by Manager.\n\n\n- Perform inspections, sample collection, container loading and other services in accordance with SOP, protocols, and client’s SOP.\n* Working location: Hồ Chí Minh/ Bình Dương/ Thái Bình/ Hải Dương\n\n\n- Examine selected samples objectively and accomplish inspection reports according to inspected results ensuring accuracy and objectivity.\n\n\n- Prepare final typed reports.\n\n\n- Support and deliver technical advice to HL inspectors and involved parties, including special requirements and updated procedure. In addition, to enhance the team development thru coaching and periodic training.\n\n\n- Participate any sort of training courses conducted by company or clients as required.\n\n\n- Perform on-site assessment for the team.\n\n\n- Stricly follow BVCPS Code of Ethics, Code of Conduct and related requirements as provided.\n\n\n- Perform other suitable duties as assigned by Manager',
    requirements:
      '- University graduated\n\n\n- Production management or Quality assurance of consumer products (furniture, handicraft, ceramic, electric, electronic…)\n\n\n- Technical training preferred\n\n\n- At least 3 year -experience in inspection/ QC\n\n\n- Knowledge of AQL system.\n\n\n- Good command of written and spoken English and local languages\n\n\n- Good communication skill\n\n\n- Capability in working under high pressure.',
  },
  {
    job_title: 'Nhân Viên Phụ Trách Kênh Bán Hàng Dự Án',
    job_url:
      'https://www.vietnamworks.com/nhan-vien-phu-trach-kenh-ban-hang-du-an-1766883-jv?source=searchResults&searchType=2&placement=1770433&sortBy=latest',
    company_name: 'Công Ty Cổ Phần Máy - Thiết Bị Dầu Khí (PV Machino)',
    company_url:
      'https://www.vietnamworks.com/nha-tuyen-dung/cong-ty-co-phan-may-thiet-bi-dau-khi-pv-machino-c165881?fromPage=jobDetail',
    location: 'Hàng Trống, Hoàn Kiếm, Hà Nội',
    post_date: new Date(1713286800),
    due_date: new Date(1716310800),
    fields: 'Kinh Doanh > Bán Hàng/Phát Triển Kinh Doanh',
    salary: 'Thương lượng',
    experience: null,
    position: 'Nhân viên',
    benefits: [
      'Thưởng\nLương, thưởng theo quy chế, kết quả kinh doanh của Công ty',
      'Chăm sóc sức khoẻ\nBHXH, BHYTcùng những chế độ khác theo quy định của Nhà nước',
      'Hoạt động nhóm\nMôi trường làm việc năng động, thân thiện, được tạo cơ hội phát triển nghề nghiệp',
    ],
    job_description:
      '* Mô tả công việc.\n- Tìm kiếm các dự án, các Chủ đầu tư và chăm sóc, tiếp cận để bán sản phẩm.\n- Xây dựng, phát triển mối quan hệ với Chủ đầu tư, Nhà thầu, Hội thiết kế kiến trúc sư để bán hàng.\n- Xây dựng phương án giá, báo giá, thương thảo, thực hiện hợp đồng.',
    requirements:
      '* Yêu cầu:\n- Số lượng: 02 người.\n- Giới tính: Nam/Nữ tuổi từ 26-40 tuổi.\n- Trình độ chuyên môn: Tốt nghiệp Cao Đẳng, Đại học.\n- Có kinh nghiệm tại vị trí tương đương, yêu thích kinh doanh và khả năng làm việc độc lập. Ưu tiên ứng viên biết Tiếng Anh, am hiểu về bán hàng các ngành điện, nội thất, vật liệu xây dựng...\n\n* Chế độ đãi ngộ.\n- Mức thu nhập hấp dẫn theo năng lực và khả năng đóng góp (Lương cơ bản, công tác phí, thưởng doanh thu không hạn chế), chi tiết trao đổi khi phỏng vấn.\n- Đóng bảo hiểm theo Luật Lao động. Nghỉ Lễ, tết theo quy định của Nhà nước.\n* Địa điểm làm việc: Hà Nội.',
  },
  {
    job_title: '[Urgent] Business Development',
    job_url:
      'https://www.vietnamworks.com/urgent-business-development--1766937-jv?source=searchResults&searchType=2&placement=1770487&sortBy=latest',
    company_name: 'Navigos Search',
    company_url:
      'https://www.vietnamworks.com/nha-tuyen-dung/navigos-search-c192082?fromPage=jobDetail',
    location: 'Pham Van Bach Street, Dich Vong Ward, Cau Giay District, Hanoi',
    post_date: new Date(1713286800),
    due_date: new Date(1716310800),
    fields: 'Kinh Doanh > Bán Hàng/Phát Triển Kinh Doanh',
    salary: '$1000 - $1500',
    experience: '5 năm kinh nghiệm',
    position: 'Nhân viên',
    benefits: [
      'Thưởng\n13th monthly salary, Performance Bonus',
      'Chăm sóc sức khoẻ\nHealthcare Plan',
      'Khác\nCompetitive package',
    ],
    job_description:
      "- Seek potential customers, introduce, consult, and promote the company's Consolidated Financial Statement (CFS) solutions and services.\n- Directly negotiate contracts, coordinate implementation, and provide post-sales customer support.\n- Develop sales plans according to assignments and the overall team's plan.\n- Keep updated on market trends and competitors.\n- Regularly communicate with product teams to receive updates on new features; closely coordinate with the marketing department for product communication.\n- Seek, maintain, and develop relationships with customers, partners, and agents to support sales.",
    requirements:
      "• Bachelor's degree, preferably in Accounting - Auditing, Finance, Economics, or Banking.\n• Experience in Accounting - Auditing, Financial Statement Consolidation.\n• Minimum 4 years of experience in Business Development with Enterprise clients in Accounting - Auditing, Finance, and Technology.\n• Passion for sales and passion for technology.\n• Enthusiastic, energetic, eager to learn.\n• Ability to work in teams, and handle pressure well.\n• Good communication and presentation skills.",
  },
];
const RecommendPage = () => {
  // //Set state of fitlers
  // //(If click on filter button, the filter component will be shown
  // //and the state will be set to true, otherwise it will be false)
  // const [showFilter, setShowFilter] = useState(true);
  // //Prevent animation when render new page
  // const [animateFilter, setAnimateFilter] = useState(false);
  // const handleClick = () => {
  //   setShowFilter(!showFilter);
  //   setAnimateFilter(true);
  // };

  // //Mock data of filters
  // const data = {
  //   major: { id: 1 },
  //   location: { id: 2 },
  //   salaryRange: { id: 3 },
  // };

  //Pagination params
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(5);
  const [totalPage, setTotalPage] = useState(10);

  //Page change when click on pagination
  const onPageChange = (page) => {
    setCurrentPage(page);
  };

  //Set state of fitlers
  const [filter, setFilter] = useState(new Set([]));
  const filterOptions = [
    { id: 1, option: 'Newest' },
    { id: 2, option: 'Oldest' },
  ];

  //Selected job description data
  const [selectedJob, setSelectedJob] = useState(sampleJobData[0]);

  //Onchange when click item in job list
  const onJobChose = (job) => {
    setSelectedJob(job);
  };

  //CV state
  const [cvFile, setCvFile] = useState([]);
  const [uploadedcvLink, setUploadedCvLink] = useState(undefined); //uploaded cv file link
  //useUser hook
  const { onGetCv, onPostCv } = useUser();

  const uploadedcvFileFunc = async () => {
    await onGetCv((response) => {
      setUploadedCvLink(response.data.data.download_url);
    });
  };

  useEffect(() => {
    uploadedcvFileFunc();
  }, []);

  //CV modal state
  const [open, setOpen] = useState(false);

  const onUploadingCv = async () => {
    if (cvFile.length > 0) {
      console.log('uploading', cvFile[0]);
      const formData = new FormData();
      formData.append('file', cvFile[0]);

      try {
        const response = await onPostCv(formData, (response) => {
          console.log(response.data);
          //Get url of uploaded cv file
          uploadedcvFileFunc();
        });

        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    }
  };

  //Job description modal state
  const [showJobDescriptionModal, setShowJobDescriptionModal] = useState(false);

  return (
    <div className="w-full h-full flex flex-col justify-center items-center gap-4">
      {!uploadedcvLink ? (
        <div className="w-full h-fit flex flex-col justify-center items-center pt-8 gap-4">
          <p className="text-[#858585]">
            Upload your CV to find the best jobs for you
          </p>

          <Button
            radius="sm"
            color="primary"
            size="lg"
            aria-label="Upload your CV"
            className="w-[35%] md:w-[25%] lg:w-[20%] xl:w-[15%] text-sm lg:text-large"
            startContent={AssetSvg.upload()}
            onClick={() => {
              onUploadingCv();
              setOpen(true);
            }}
          >
            Upload your CV
          </Button>
        </div>
      ) : (
        <div className="w-full h-fit flex flex-col items-center justify-center gap-4">
          <div className="w-full h-fit flex flex-col justify-center items-center gap-5 mt-8">
            <Button
              as={Link}
              href={uploadedcvLink}
              color="primary"
              showAnchorIcon
            >
              Your CV Link
            </Button>

            {/* <FileCard
                key={'cv'}
                files={cvFile}
                setFiles={setCvFile}
                file={cvFile[0]}
              />
              <div className="w-full h-fit flex flex-row mt-3 text-black justify-center items-center gap-8 font-bold">
                <span>Chỉnh sửa lần cuối</span>
                <span>{lastModifiedTime?.toLocaleString()}</span>
              </div> */}
            <div className="w-full h-fit flex flex-row justify-center items-center gap-4">
              <Button
                className={`
             border-orange w-32 m-4`}
                variant="bordered"
                radius="sm"
                onClick={() => {
                  setOpen(true);
                }}
              >
                Modify
              </Button>
              <Button
                className={`
                  bg-orange
             border-orange w-32 m-4`}
                variant="bordered"
                radius="sm"
                onClick={onUploadingCv}
              >
                Save
              </Button>
            </div>
          </div>
        </div>
      )}

      <div className="flex h-0 w-0 flex-col gap-y-4 justify-center overflow-hidden">
        <div className="flex flex-row gap-x-4 items-center font-bold ">
          <FileDialog
            className="text-black"
            name="Images"
            maxFiles={1}
            maxSize={1024 * 1024 * 4}
            files={cvFile}
            setFiles={setCvFile as any}
            disabled={false}
            open={open}
            onOpenChange={() => setOpen(false)}
          />
        </div>
      </div>

      {/* <div className="w-full h-fit flex flex-col items-center justify-center gap-5 mt-4">
        <div className="w-[80%] h-fit flex flex-row items-center gap-5 mt-4">
          <Input
            aria-label="Search for jobs"
            variant="bordered"
            color={'primary'}
            size={'lg'}
            isClearable
            radius="lg"
            classNames={{
              label: 'text-black/50 dark:text-white/90',
              input: [
                'bg-transparent',
                'text-black',
                'placeholder:text-default-700/50 dark:placeholder:text-slate/60',
                'border-primary',
              ],
              innerWrapper: 'bg-transparent',
              inputWrapper: [
                'shadow-lg',
                'bg-white',
                'border-primary',
                'backdrop-blur-xl',
                'hover:bg-secondary',
                'dark:hover:bg-default/70',
                'group-data-[focused=true]:bg-default-200/50',
                'dark:group-data-[focused=true]:bg-default/60',
                '!cursor-text',
              ],
            }}
            placeholder="Type to search..."
            startContent={AssetSvg.search({
              className:
                'text-primary mb-0.5 pointer-events-none flex-shrink-0',
            })}
          />
          <Button
            radius="sm"
            color="primary"
            size="lg"
            className="w-[10%]"
            aria-label="Search"
          >
            Search
          </Button>
        </div>
        <div className="w-[80%] h-fit">
          <Button
            radius="sm"
            variant="bordered"
            color="primary"
            className="w-[15%]"
            aria-label="Filter"
            startContent={AssetSvg.filter()}
            onClick={handleClick}
          >
            Filter
          </Button>
        </div>

        <div
          className={`w-[80%] h-fit ${
            animateFilter && showFilter
              ? 'animate-appearance-in duration-500'
              : ' '
          }`}
          style={{ height: showFilter ? 'auto' : '0', overflow: 'hidden' }}
        >
          <Filter data={data} isOpen={showFilter} />
        </div>
      </div> */}

      <div className="w-full h-fit flex flex-row gap-3 bg-secondary mt-8 z-0">
        <div className="w-[50%] h-full mx-8 my-16 flex flex-col z-10">
          <div className="w-full h-fit flex flex-row justify-between items-center">
            <p className="font-bold text-lg text-black">
              {sampleJobData.length} Jobs
            </p>
            <Select
              className="w-fit"
              style={{ width: '15rem' }}
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
                  className={`{text-black }`}
                  onMouseEnter={() => {}}
                >
                  {c.option}
                </SelectItem>
              ))}
            </Select>
          </div>
          {sampleJobData ? (
            <div className="w-full flex flex-col justify-center items-center">
              {' '}
              {/* {isFetching ? (
              <Spinner
                className=""
                label="Đang tải..."
                color="warning"
                labelColor="warning"
              />
            ) : ( */}
              {
                <div className="w-full h-fit z-0">
                  {sampleJobData?.map((item) => (
                    <div
                      key={item.job_url}
                      className={`w-full h-fit flex flex-row items-center justify-between my-2 relative ${
                        showJobDescriptionModal &&
                        selectedJob.job_url === item.job_url
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
                    >
                      <JobListItem
                        data={item}
                        isSelected={selectedJob.job_url === item.job_url}
                      />{' '}
                      {showJobDescriptionModal &&
                        selectedJob.job_url === item.job_url && (
                          <div className="z-10 absolute -top-16 right-0 w-1/5">
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
                total={totalPage}
                initialPage={1}
                onChange={(page) => {
                  onPageChange(page);
                }}
                page={currentPage}
              />
            </div>
          ) : null}
        </div>

        <div className="z-0 w-[50%] h-[600px] mx-8 my-16 flex flex-col rounded-lg bg-white">
          <div className="h-[80%] w-full flex flex-col ">
            <ChatHeader></ChatHeader>
            <ChatMessages></ChatMessages>
          </div>

          <ChatInput className="w-full h-[15%] p-3 z-0"></ChatInput>
        </div>

        {/* <div className="w-[50%] h-full mx-8 my-16">
          <JobDescriptionCard data={selectedJob}></JobDescriptionCard>
        </div> */}
      </div>
    </div>
  );
};

export default RecommendPage;
