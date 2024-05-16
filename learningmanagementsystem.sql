/*
 Navicat Premium Data Transfer

 Source Server         : sms
 Source Server Type    : MySQL
 Source Server Version : 50744 (5.7.44-log)
 Source Host           : localhost:3306
 Source Schema         : learningmanagementsystem

 Target Server Type    : MySQL
 Target Server Version : 50744 (5.7.44-log)
 File Encoding         : 65001

 Date: 19/04/2024 17:12:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for administrator
-- ----------------------------
DROP TABLE IF EXISTS `administrator`;
CREATE TABLE `administrator`  (
  `AdminID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `Password` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`AdminID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 202403 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of administrator
-- ----------------------------
INSERT INTO `administrator` VALUES (123401, 'Annie', 'a123');
INSERT INTO `administrator` VALUES (123402, 'Zoe', 'a123');

-- ----------------------------
-- Table structure for assignment
-- ----------------------------
DROP TABLE IF EXISTS `assignment`;
CREATE TABLE `assignment`  (
  `AssignmentID` int(11) NOT NULL AUTO_INCREMENT,
  `AssignmentTitle` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `Deadline` date NULL DEFAULT NULL,
  `CourseID` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`AssignmentID`) USING BTREE,
  INDEX `CourseID`(`CourseID`) USING BTREE,
  CONSTRAINT `assignment_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `course` (`CourseID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of assignment
-- ----------------------------

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course`  (
  `CourseID` int(11) NOT NULL AUTO_INCREMENT,
  `CourseTitle` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `Content` text CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  `CreditHours` int(11) NULL DEFAULT NULL,
  `InstructorID` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`CourseID`) USING BTREE,
  INDEX `InstructorID`(`InstructorID`) USING BTREE,
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`InstructorID`) REFERENCES `instructor` (`InstructorID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course
-- ----------------------------

-- ----------------------------
-- Table structure for discussionforum
-- ----------------------------
DROP TABLE IF EXISTS `discussionforum`;
CREATE TABLE `discussionforum`  (
  `ForumID` int(11) NOT NULL AUTO_INCREMENT,
  `CourseID` int(11) NULL DEFAULT NULL,
  `Title` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `Description` text CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  PRIMARY KEY (`ForumID`) USING BTREE,
  INDEX `CourseID`(`CourseID`) USING BTREE,
  CONSTRAINT `discussionforum_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `course` (`CourseID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of discussionforum
-- ----------------------------

-- ----------------------------
-- Table structure for enrollment
-- ----------------------------
DROP TABLE IF EXISTS `enrollment`;
CREATE TABLE `enrollment`  (
  `EnrollmentID` int(11) NOT NULL AUTO_INCREMENT,
  `StudentID` int(11) NULL DEFAULT NULL,
  `CourseID` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`EnrollmentID`) USING BTREE,
  INDEX `StudentID`(`StudentID`) USING BTREE,
  INDEX `CourseID`(`CourseID`) USING BTREE,
  CONSTRAINT `enrollment_ibfk_1` FOREIGN KEY (`StudentID`) REFERENCES `student` (`StudentID`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `enrollment_ibfk_2` FOREIGN KEY (`CourseID`) REFERENCES `course` (`CourseID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of enrollment
-- ----------------------------

-- ----------------------------
-- Table structure for instructor
-- ----------------------------
DROP TABLE IF EXISTS `instructor`;
CREATE TABLE `instructor`  (
  `InstructorID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `Password` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`InstructorID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 999902 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of instructor
-- ----------------------------
INSERT INTO `instructor` VALUES (999901, 'Nicole', 'a123');

-- ----------------------------
-- Table structure for lecture
-- ----------------------------
DROP TABLE IF EXISTS `lecture`;
CREATE TABLE `lecture`  (
  `LectureID` int(11) NOT NULL AUTO_INCREMENT,
  `CourseID` int(11) NULL DEFAULT NULL,
  `LectureTitle` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `UploadDate` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`LectureID`) USING BTREE,
  INDEX `CourseID`(`CourseID`) USING BTREE,
  CONSTRAINT `lecture_ibfk_1` FOREIGN KEY (`CourseID`) REFERENCES `course` (`CourseID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of lecture
-- ----------------------------

-- ----------------------------
-- Table structure for post
-- ----------------------------
DROP TABLE IF EXISTS `post`;
CREATE TABLE `post`  (
  `PostID` int(11) NOT NULL AUTO_INCREMENT,
  `ForumID` int(11) NULL DEFAULT NULL,
  `PostedBy` int(11) NOT NULL,
  `Content` text CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  `PostDate` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`PostID`) USING BTREE,
  INDEX `ForumID`(`ForumID`) USING BTREE,
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`ForumID`) REFERENCES `discussionforum` (`ForumID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of post
-- ----------------------------

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `StudentID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `Major` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `Password` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`StudentID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20210102 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES (20210101, 'Dalla', NULL, 'a123');

-- ----------------------------
-- Table structure for submission
-- ----------------------------
DROP TABLE IF EXISTS `submission`;
CREATE TABLE `submission`  (
  `SubmissionID` int(11) NOT NULL AUTO_INCREMENT,
  `AssignmentID` int(11) NULL DEFAULT NULL,
  `StudentID` int(11) NULL DEFAULT NULL,
  `SubmitDate` date NULL DEFAULT NULL,
  `Grade` decimal(5, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`SubmissionID`) USING BTREE,
  INDEX `AssignmentID`(`AssignmentID`) USING BTREE,
  INDEX `StudentID`(`StudentID`) USING BTREE,
  CONSTRAINT `submission_ibfk_1` FOREIGN KEY (`AssignmentID`) REFERENCES `assignment` (`AssignmentID`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `submission_ibfk_2` FOREIGN KEY (`StudentID`) REFERENCES `student` (`StudentID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of submission
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
