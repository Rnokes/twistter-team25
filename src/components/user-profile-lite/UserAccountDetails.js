import React, { useState } from "react";
import {
  Card,
  CardHeader,
  ListGroup,
  ListGroupItem,
  Row,
  Col,
  Form,
  FormInput,
  FormTextarea,
  Button
} from "shards-react";
import { Link } from "react-router-dom";
import Alert from "react-bootstrap/Alert";
const axios = require("axios");

export default class UserAccountDetails extends React.Component {
  constructor() {
    super();

    this.state = {
      UserName: "kbuzza",
      Password:
        "AgAAAL3TGAwoCfdc9WzoMWuCya/6t3+9qUHeULhpxwcy+VBSPuaySpwyCAcOgFo5FntJfQ==",
      CommonName: "Kyle",
      Email: "kbuzza@purdue.edu",
      Description: "This is my description."
    };
    this.handleName = this.handleName.bind(this);
    this.handleFirstPassword = this.handleFirstPassword.bind(this);
    this.handleSecondPassword = this.handleSecondPassword.bind(this);
    this.handleDescription = this.handleDescription.bind(this);
    this.submitForm = this.submitForm.bind(this);
    this.updateUserDetails = this.updateUserDetails.bind(this);
  }

  async updateUserDetails(post_data) {
    // user-update-common-name
    let newName = JSON.stringify({
      userId: global.ValidatedUser,
      newCommonName: post_data.newCommonName
    });
    const common_name_response = axios.post(
      //"http://twistter-API.azurewebsites.net/user-update-common-name",
      "http://localhost:5000/user-update-common-name",
      newName
    );
    console.log(common_name_response);

    // user-update-description
    let newDesc = JSON.stringify({
      userId: global.ValidatedUser,
      newDescription: post_data.newDescription
    });
    const description_response = axios.post(
      //"http://twistter-API.azurewebsites.net/user-update-description",
      "http://localhost:5000/user-update-description",
      newDesc
    );
    console.log(description_response);

    // update-password if applicable
    if (post_data.newPassword !== undefined) {
      let newPass = JSON.stringify({
        userId: global.ValidatedUser,
        newPassword: post_data.newPassword
      });
      const password_response = axios.post(
        //"http://twistter-API.azurewebsites.net/update-password",
        "http://localhost:5000/update-password",
        newPass
      );
      console.log(password_response);
    }
  }

  async componentDidMount() {
    let config = {
      headers: {
        "content-type": "application/json"
      }
    };

    let data = JSON.stringify({ userId: global.ValidatedUser });
    if (global.ValidatedUser !== -1) {
      const response = await axios.post(
        //"http://twistter-API.azurewebsites.net/get-user",
        "http://localhost:5000/get-user",
        data,
        config
      );
      console.log(response.data);
      this.setState(response.data);
    }
  }

  submitForm() {
    if (
      !this.state.FirstPassword === undefined &&
      this.state.SecondPassword === undefined
    ) {
      this.setState({ passwordInvalid: true });
    } else if (
      this.state.FirstPassword === undefined &&
      !this.state.SecondPassword === undefined
    ) {
      this.setState({ passwordInvalid: true });
    } else if (
      this.state.FirstPassword === undefined &&
      this.state.SecondPassword === undefined
    ) {
      this.setState({ passwordInvalid: false });
    } else if (
      this.state.FirstPassword.localeCompare(this.state.SecondPassword) != 0
    ) {
      this.setState({ passwordInvalid: true });
    } else if (
      this.state.FirstPassword.localeCompare(this.state.SecondPassword) == 0 &&
      validate_password(this.state.FirstPassword) == true
    ) {
      this.setState({ passwordInvalid: false });
    } else {
      this.setState({ passwordInvalid: true });
    }

    var userSubmission = {};
    if (this.state.passwordInvalid == false) {
      /* Random lowercase shit is to communicate with the api better */
      var userSubmission = {
        UserName: this.state.UserName,
        newCommonName: this.state.CommonName,
        Email: this.state.Email,
        newDescription: this.state.Description
      };

      if (this.state.FirstPassword === undefined) {
      } else {
        userSubmission.newPassword = this.state.FirstPassword;
      }
      //TODO: COMMUNICATE WITH API
      this.updateUserDetails(userSubmission);
      console.log(userSubmission);
    }
  }

  handleName(e) {
    this.setState({ CommonName: e.target.value });
  }

  handleFirstPassword(e) {
    this.setState({ FirstPassword: e.target.value });
  }

  handleSecondPassword(e) {
    this.setState({ SecondPassword: e.target.value });
  }

  handleDescription(e) {
    this.setState({ Description: e.target.value });
  }

  render() {
    return (
      <Card small className="mb-4" bg="secondary">
        <CardHeader className="border-bottom">
          <h6 className="m-0">Account Details</h6>
        </CardHeader>
        <ListGroup flush>
          <ListGroupItem className="p-3">
            <Col>
              <Form>
                <Row form>
                  {/* Name */}
                  <Col md="6" className="form-group">
                    <label htmlFor="DisplayName">Display Name</label>
                    <FormInput
                      id="DisplayName"
                      name="DisplayName"
                      placeholder="Display Name"
                      defaultValue={this.state.CommonName}
                      onChange={this.handleName}
                    />
                  </Col>
                </Row>
                <Row form>
                  {/* Password */}
                  <Col md="6" className="form-group">
                    <label htmlFor="Password">Change Password</label>
                    <FormInput
                      type="password"
                      id="Password"
                      name="Password"
                      placeholder="Password"
                      onChange={this.handleFirstPassword}
                      autoComplete="current-password"
                    />
                    <label htmlFor="PasswordConfirm">
                      Confirm Password Change
                    </label>
                    <FormInput
                      type="password"
                      id="PasswordConfirm"
                      name="PasswordConfirm"
                      placeholder="Password"
                      onChange={this.handleSecondPassword}
                      autoComplete="current-password"
                    />
                    {this.state.passwordInvalid && (
                      <div>
                        <p>Passwords must match and be valid strings!</p>
                        <p>
                          Password must be 8-20 characters and contain at least
                          one uppercase, lowercase, number, and special
                          character.
                        </p>
                      </div>
                    )}
                  </Col>
                </Row>
                <Row form>
                  {/* Description */}
                  <Col md="12" className="form-group">
                    <label htmlFor="Description">Description</label>
                    <FormTextarea
                      id="Description"
                      name="Description"
                      defaultValue={this.state.Description}
                      placeholder="Description"
                      rows="5"
                      onChange={this.handleDescription}
                    />
                  </Col>
                </Row>
                <Row>
                  <Col>
                    <Button theme="dark" onClick={this.submitForm}>
                      Update Account
                    </Button>
                  </Col>
                  <Col>
                    <DeleteAccountButton deleteUser={this.deleteUser} />
                  </Col>
                </Row>
              </Form>
            </Col>
          </ListGroupItem>
        </ListGroup>
      </Card>
    );
  }
}
async function deleteUser() {
  let userToDelete = JSON.stringify({
    userId: global.ValidatedUser
  });
  console.log("DELETE");
  console.log(userToDelete);
  const userDeleteResponse = axios.post(
    //"http://twistter-API.azurewebsites.net/user-delete",
    "http://localhost:5000/user-delete",
    userToDelete
  );
  console.log(userDeleteResponse);
}

function DeleteAccountButton() {
  const [show, setShow] = useState(false);

  return (
    <div>
      <Alert variant="danger" show={show}>
        <Alert.Heading>WARNING</Alert.Heading>
        <p>CONTINUING WILL PERMANENTLY DELETE YOUR ACCOUNT!</p>
        <hr />
        <Link to="/login">
          <Button onClick={deleteUser}>
            Yes, I would like to permanently delete my account! This will route
            you back to the login page.
          </Button>
        </Link>
      </Alert>

      {!show && (
        <Button className="float-right" onClick={() => setShow(true)}>
          Delete Account
        </Button>
      )}
    </div>
  );
}

/* Validates a password that is passed into the function with the following parameters:
 * At least one uppercase letter, one lowercase letter, one number, one special
 * character, with a total length between 8 and 20 characters, inclusive.
 * TODO: clean password inputs and make sure that no SQL injection is possible.
 *
 * Returns true if password is valid, false otherwise.
 */

function validate_password(pass) {
  if (typeof pass === "undefined" || pass === "") {
    return true;
  }
  return /^(?=.*[a-z])+(?=.*[A-Z])+(?=.*\d)+(?=.*[~`!@#$%^&*()_\-+=:?])+[A-Za-z\d~`!@#$%^&*()_\-+=:?]{8,20}$/.test(
    pass
  );
}
