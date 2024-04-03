-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 27, 2024 at 08:15 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `medical_bot_new`
--

-- --------------------------------------------------------

--
-- Table structure for table `cc_admin`
--

CREATE TABLE `cc_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cc_admin`
--

INSERT INTO `cc_admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `cc_data`
--

CREATE TABLE `cc_data` (
  `id` int(11) NOT NULL,
  `user_query` varchar(200) NOT NULL,
  `response1` text NOT NULL,
  `response2` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cc_data`
--

INSERT INTO `cc_data` (`id`, `user_query`, `response1`, `response2`) VALUES
(1, 'How do you detect a heart attack?', 'This first test done to diagnose a heart attack records electrical signals as they travel through the heart.', 'Sticky patches (electrodes) are attached to the chest and sometimes the arms and legs. '),
(2, 'What are the 4 stages of diabetes?', 'Diabetes occurs in four stages: Insulin resistance, prediabetes, type 2 diabetes, and type 2 diabetes with vascular complications.', 'You are at higher risk for these conditions if you are older than 45, have close biological relatives with diabetes.');

-- --------------------------------------------------------

--
-- Table structure for table `cc_disease`
--

CREATE TABLE `cc_disease` (
  `id` int(11) NOT NULL,
  `disease` varchar(100) NOT NULL,
  `symptom1` varchar(100) NOT NULL,
  `symptom2` varchar(100) NOT NULL,
  `symptom3` varchar(100) NOT NULL,
  `symptom4` varchar(100) NOT NULL,
  `symptom5` varchar(100) NOT NULL,
  `test1` varchar(50) NOT NULL,
  `test2` varchar(50) NOT NULL,
  `consultant` varchar(50) NOT NULL,
  `user_query` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cc_disease`
--

INSERT INTO `cc_disease` (`id`, `disease`, `symptom1`, `symptom2`, `symptom3`, `symptom4`, `symptom5`, `test1`, `test2`, `consultant`, `user_query`) VALUES
(1, 'Diarrhea', 'Vomiting', 'Fever', 'Abdominal Pain', 'Nausea', 'Bloating', 'Stool test', 'Blood test', 'General Physican', 'what are the symptoms for Diarrhea?, what test needed for diarrhea'),
(2, 'Asthma', 'Wheezing', 'Breathlessness', 'Tight Chest', 'Caughing', 'Sleeplessness', 'CT scan ', 'Blood test', 'Dermatologist', ''),
(3, 'Covid', 'Fever', 'Dry caugh', 'sore throat', 'taste/ smell loss', 'Chest pain', 'PCR test', 'Antigen test', 'General Physican', ''),
(4, 'Parkinson', 'Slowed movement', 'Tremor', 'Rigid Muscle', 'Speech Change', 'Writing change', 'Blood test', 'MRI', 'Neurologist', ''),
(5, 'Malaria', 'Vomiting', 'Nausea', 'Tiredness', 'Muscle aches', 'Headache', 'Antigen test', 'PCR test', 'General Physican', ''),
(6, 'Diabetes', 'Thirsty', 'Lose weight', 'Frequent urination', 'Frequenlty hungry', 'Blurry vision', 'Sugur test', 'Glucose test', 'Endocrinologist', 'What is the main cause of diabetes?'),
(7, 'Allergy', 'Sneezing', 'Eye irritation', 'Tummy pain ', 'Red resh', 'Cracked skin', 'Blood test', 'SPT ', 'Dermatologist', ''),
(8, 'Influenza', 'Fever', 'sore throat ', 'Stuffy nose', 'Fatigue', ' Body aches', 'RT-PCR test', 'Viral Culture test', 'General Physican', ''),
(9, 'Heart Attack', 'Chest pain', 'Weakness', 'Shortness of breath', ' feeling Nauseous', ' Light headed', 'ECG', 'Blood test', 'Cardiologist', ''),
(10, 'Ulcer', 'Dark stool', 'Vomiting', 'Heart burning', 'Burping', 'pain in back', 'X-ray', 'Endoscopy', 'Gastroenterologist', '');

-- --------------------------------------------------------

--
-- Table structure for table `cc_image`
--

CREATE TABLE `cc_image` (
  `id` int(11) NOT NULL,
  `img_name` varchar(100) NOT NULL,
  `disease` text NOT NULL,
  `img_type` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cc_image`
--

INSERT INTO `cc_image` (`id`, `img_name`, `disease`, `img_type`) VALUES
(1, 'r15.jpg', 'Brain Tumor, Stage2', 'brain tumor'),
(2, 'r21.jpg', 'Brain Tumor, Severe Stage', 'brain tumor'),
(3, 'r10.jpg', 'Kidney Disease', 'kidney'),
(4, 'ty4d-pn.jpeg', 'Pneumonia', 'pneumonia');

-- --------------------------------------------------------

--
-- Table structure for table `cc_location`
--

CREATE TABLE `cc_location` (
  `id` int(11) NOT NULL,
  `hospital` varchar(100) NOT NULL,
  `specialist` varchar(100) NOT NULL,
  `location` varchar(50) NOT NULL,
  `city` varchar(30) NOT NULL,
  `treatment` varchar(100) NOT NULL,
  `doctor_link` varchar(200) NOT NULL,
  `user_query` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cc_location`
--

INSERT INTO `cc_location` (`id`, `hospital`, `specialist`, `location`, `city`, `treatment`, `doctor_link`, `user_query`) VALUES
(1, 'Diabetes Specialities Centre', 'Dr.Mohan', '2ND FLOOR, TBR TOWERS', 'Trichy', 'Diabetes', 'https://meet.google.com/nkr-xvoa-kqx', ''),
(2, 'M.V Hospital', 'Dr.Viswa', 'Diabetes', 'https://meet.google.com/nkr-xv', 'No.4 W Madha Church St.', 'Chennai', 'diabetes treatment'),
(3, 'KMC', 'Dr.S.Raghu', 'Tennur', 'Trichy', 'Heart Attack, Cardiology', 'https://meet.google.com/nkr-xvoa-kqx', ''),
(4, 'GS Heart Clinic', 'Dr.G.Sengottuvelu', 'T.Nagar', 'Chennai', 'Heart Attack, Cardiology', 'https://meet.google.com/nkr-xvoa-kqx', ''),
(5, 'Neuro Foundation Hospital', 'Dr.K.Subash', 'Meyyanur Main Rd', 'Salem', 'brain tumor', 'https://meet.google.com/nkr-xvoa-kqx', '');

-- --------------------------------------------------------

--
-- Table structure for table `cc_medicine`
--

CREATE TABLE `cc_medicine` (
  `id` int(11) NOT NULL,
  `medicine` varchar(100) NOT NULL,
  `uses` text NOT NULL,
  `dosage` text NOT NULL,
  `side_effect` text NOT NULL,
  `special` text NOT NULL,
  `user_query` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cc_medicine`
--

INSERT INTO `cc_medicine` (`id`, `medicine`, `uses`, `dosage`, `side_effect`, `special`, `user_query`) VALUES
(1, 'Metformin', 'It works by decreasing the production of glucose in the liver and increasing the sensitivity of muscle cells to insulin, thereby improving glucose utilization.', 'Usual Adult Dose for Diabetes Type 2. Immediate-release: Initial dose: 500 mg orally twice a day or 850 mg orally once a day.', 'General feeling of being unwell with severe tiredness, fast or shallow breathing, being cold and a slow heartbeat.', 'Metformin should be taken with meals to help reduce stomach or bowel side effects that may occur during the first few weeks of treatment.', 'Diabetes medicine'),
(2, 'Aspirin', 'Aspirin helps get more blood flowing to your legs. It can treat a heart attack and prevent blood clots when you have an abnormal heartbeat. You probably will take aspirin after you have treatment for clogged arteries.', ' Oral: 300 to 650 mg orally every 4 to 6 hours as needed. Maximum dose: 4 g in 24 hours', 'the whites of your eyes turn yellow or your skin turns yellow, this can be a sign of liver problems. the joints in your hands and feet are painful.', 'tell your doctor if you often have heartburn, upset stomach, or stomach pain and if you have or have ever had ulcers, anemia, bleeding problems such as hemophilia, or kidney or liver disease', 'Heart Attack medicine');

-- --------------------------------------------------------

--
-- Table structure for table `cc_register`
--

CREATE TABLE `cc_register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `location` varchar(30) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `otp` varchar(10) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cc_register`
--

INSERT INTO `cc_register` (`id`, `name`, `mobile`, `email`, `location`, `uname`, `pass`, `create_date`, `otp`, `status`) VALUES
(1, 'Vijay', 9638527415, 'vijay@gmail.com', 'Trichy', 'vijay', '1234', '', '', 0),
(2, 'Santhosh', 9895445274, 'santhosh@gmail.com', 'Salem', 'santhosh', '123456', '', '', 0),
(3, 'Varun', 7854584656, 'varun@gmail.com', 'Chennai', 'varun', '1234', '', '', 0);
