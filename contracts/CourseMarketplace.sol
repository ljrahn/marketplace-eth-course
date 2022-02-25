// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

contract CourseMarketplace {
  enum State {
    Purchased,
    Activated,
    Deactivated
  }

  // mapping of courseHash to Course data
  mapping(bytes32 => Course) private ownedCourses;

  // Mapping of courseID to courseHash
  mapping(uint => bytes32) private ownedCourseHash;

  // Number of all courses + id of the course
  uint private totalOwnedCourses;

  struct Course {
    uint id;
    uint price;
    bytes32 proof;
    address owner;
    State state; 

  }

  address payable private owner;

  constructor() {
    setContractOwner(msg.sender);
  }


  modifier onlyOwner() {
    require(msg.sender == getContractOwner(), 'Only owner has access to this function!');
    _;
  }

  function purchaseCourse(
    // course id - 10
    bytes16 courseId, // 0x00000000000000000000000000003130
    bytes32 proof // 0x0000000000000000000000000000313000000000000000000000000000003130
  ) external payable {

    bytes32 courseHash = keccak256(abi.encodePacked(courseId, msg.sender));

    require(!hasCourseOwnership(courseHash), 'Course already has an owner!');

    uint id = totalOwnedCourses++;

    ownedCourseHash[id] = courseHash;
    ownedCourses[courseHash] = Course({
      id: id,
      price: msg.value,
      proof: proof,
      owner: msg.sender,
      state: State.Purchased
    });
  }

  function repurchaseCourse(bytes32 courseHash) external payable {
    require(isCourseCreated(courseHash), 'Course has not been created!');
    require(hasCourseOwnership(courseHash), 'Sender is not course owner!');

    Course storage course = ownedCourses[courseHash];
    require(course.state == State.Deactivated, 'Course is not in deactivated state!');
    course.state = State.Purchased;
    course.price = msg.value;
  }

  function activateCourse(bytes32 courseHash) external onlyOwner {

    require(isCourseCreated(courseHash), 'Course has not been created!');

    Course storage course = ownedCourses[courseHash];

    require(course.state == State.Purchased, 'Course is not in purchased state!');

    course.state = State.Activated;
  }

  function deactivateCourse(bytes32 courseHash) external onlyOwner {

    require(isCourseCreated(courseHash), 'Course has not been created!');

    Course storage course = ownedCourses[courseHash];
    
    require(course.state == State.Purchased, 'Course is not in purchased state!');

    (bool success, ) = course.owner.call{value: course.price}("");
    require(success, "Transfer failed!");

    course.state = State.Deactivated;
    course.price = 0;
  }

  function transferOwnership(address newOwner) external onlyOwner {
    setContractOwner(newOwner);
  }

  function getCourseCount() public view returns(uint) {
    return totalOwnedCourses;
  }

  function getCourseHash(uint index) public view returns(bytes32) {
    return ownedCourseHash[index];
  }

  function getCourseByHash(bytes32 courseHash) public view returns(Course memory) {
    return ownedCourses[courseHash];
  }

  function getContractOwner() public view returns(address) {
    return owner;
  }

  function setContractOwner(address newOwner) private {
    owner = payable(newOwner);
  }

  function isCourseCreated(bytes32 courseHash) private view returns(bool) {
    return ownedCourses[courseHash].owner != 0x0000000000000000000000000000000000000000;
  }

  function hasCourseOwnership(bytes32 courseHash) private view returns (bool) {
    return ownedCourses[courseHash].owner == msg.sender;
  }

}