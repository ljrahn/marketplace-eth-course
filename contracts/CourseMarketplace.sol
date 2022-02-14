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

  /// Course already has an owner!
  error CourseHasOwner();

  /// Only owner has access to this function! 
  error OnlyOwner();

  modifier onlyOwner() {
    if (msg.sender != getContractOwner()) {
      revert OnlyOwner();
    }
    _;
  }

  function purchaseCourse(
    // course id - 10
    bytes16 courseId, // 0x00000000000000000000000000003130
    bytes32 proof // 0x0000000000000000000000000000313000000000000000000000000000003130
  ) external payable {

    bytes32 courseHash = keccak256(abi.encodePacked(courseId, msg.sender));

    if (hasCourseOwnership(courseHash)) {
      revert CourseHasOwner();
    }

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

  function hasCourseOwnership(bytes32 courseHash) private view returns (bool) {
    return ownedCourses[courseHash].owner == msg.sender;
  }

}