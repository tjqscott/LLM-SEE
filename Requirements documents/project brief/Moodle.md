# Moodle

Moodle is a free and open-source learning management system (LMS) written in PHP and distributed under the GNU General Public License.

1. The course instructor interacts with Moodle via a web-based administration interface to create a new digital course. They input a course title, a brief text syllabus, and a start date.
2. The instructor uploads educational assets (PDF documents or MP4 videos) to the course page. The system stores these files on the local web server disk. Assume the maximum file upload size is strictly capped at 50MB.
3. A student logs into the web interface and navigates to the course page to view the syllabus and download the assets.
4. The system logs the student's interaction in an internal relational database tracking table, recording the timestamp and the specific asset downloaded. 
5. Advanced analytics dashboards, SCORM package integration, and automated grading of interactive quizzes are out of scope for this initial learning management module.
