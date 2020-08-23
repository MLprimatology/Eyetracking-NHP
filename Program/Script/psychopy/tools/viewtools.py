#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tools for working with view projections for 2- and 3-D rendering.

"""

# Part of the PsychoPy library
# Copyright (C) 2002-2018 Jonathan Peirce (C) 2019 Open Science Tools Ltd.
# Distributed under the terms of the GNU General Public License (GPL).

__all__ = ['Frustum',
           'computeFrustum',
           'generalizedPerspectiveProjection',
           'orthoProjectionMatrix',
           'perspectiveProjectionMatrix',
           'lookAt',
           'pointToNdc',
           'cursorToRay']

import numpy as np
from collections import namedtuple
import psychopy.tools.mathtools as mt

# convenient named tuple for storing frustum parameters
Frustum = namedtuple(
    'Frustum',
    ['left', 'right', 'bottom', 'top', 'nearVal', 'farVal'])


def computeFrustum(scrWidth,
                   scrAspect,
                   scrDist,
                   convergeOffset=0.0,
                   eyeOffset=0.0,
                   nearClip=0.01,
                   farClip=100.0):
    """Calculate frustum parameters. If an eye offset is provided, an asymmetric
    frustum is returned which can be used for stereoscopic rendering.

    Parameters
    ----------
    scrWidth : float
        The display's width in meters.
    scrAspect : float
        Aspect ratio of the display (width / height).
    scrDist : float
        Distance to the screen from the view in meters. Measured from the center
        of their eyes.
    convergeOffset : float
        Offset of the convergence plane from the screen. Objects falling on this
        plane will have zero disparity. For best results, the convergence plane
        should be set to the same distance as the screen (0.0 by default).
    eyeOffset : float
        Half the inter-ocular separation (i.e. the horizontal distance between
        the nose and center of the pupil) in meters. If eyeOffset is 0.0, a
        symmetric frustum is returned.
    nearClip : float
        Distance to the near clipping plane in meters from the viewer. Should be
        at least less than scrDist.
    farClip : float
        Distance to the far clipping plane from the viewer in meters. Must be
        >nearClip.

    Returns
    -------
    Frustum
        Namedtuple with frustum parameters. Can be directly passed to
        glFrustum (e.g. glFrustum(*f)).

    Notes
    -----

    * The view point must be transformed for objects to appear correctly.
      Offsets in the X-direction must be applied +/- eyeOffset to account for
      inter-ocular separation. A transformation in the Z-direction must be
      applied to accountfor screen distance. These offsets MUST be applied to
      the GL_MODELVIEW matrix, not the GL_PROJECTION matrix! Doing so may break
      lighting calculations.

    Examples
    --------

    Creating a frustum and setting a window's projection matrix::

        scrWidth = 0.5  # screen width in meters
        scrAspect = win.size[0] / win.size[1]
        scrDist = win.scrDistCM * 100.0  # monitor setting, can be anything
        frustum = viewtools.computeFrustum(scrWidth, scrAspect, scrDist)

    Accessing frustum parameters::

        left, right, bottom, top, nearVal, farVal = frustum
        # ... or ...
        left = frustum.left

    Off-axis frustums for stereo rendering::

        # compute view matrix for each eye, these value usually don't change
        eyeOffset = (-0.035, 0.035)  # +/- IOD / 2.0
        scrDist = 0.50  # 50cm
        scrWidth = 0.53  # 53cm
        scrAspect = 1.778
        leftFrustum = viewtools.computeFrustum(scrWidth, scrAspect, scrDist, eyeOffset[0])
        rightFrustum = viewtools.computeFrustum(scrWidth, scrAspect, scrDist, eyeOffset[1])
        # make sure your view matrix accounts for the screen distance and eye offsets!

    Using computed view frustums with a window::

        win.projectionMatrix = viewtools.perspectiveProjectionMatrix(*frustum)
        # generate a view matrix looking ahead with correct viewing distance,
        # origin is at the center of the screen. Assumes eye is centered with
        # the screen.
        eyePos = [0.0, 0.0, scrDist]
        screenPos = [0.0, 0.0, 0.0]  # look at screen center
        eyeUp = [0.0, 1.0, 0.0]
        win.viewMatrix = viewtools.lookAt(eyePos, screenPos, eyeUp)
        win.applyViewTransform()  # call before drawing

    """
    # mdc - uses display size instead of the horizontal FOV gluPerspective needs
    d = scrWidth / 2.0
    ratio = nearClip / float((convergeOffset + scrDist))

    right = (d - eyeOffset) * ratio
    left = (d + eyeOffset) * -ratio
    top = d / float(scrAspect) * ratio
    bottom = -top

    return Frustum(left, right, bottom, top, nearClip, farClip)


def generalizedPerspectiveProjection(posBottomLeft,
                                     posBottomRight,
                                     posTopLeft,
                                     eyePos,
                                     nearClip=0.01,
                                     farClip=100.0,
                                     dtype=None):
    """Generalized derivation of projection and view matrices based on the
    physical configuration of the display system.

    This implementation is based on Robert Kooima's 'Generalized Perspective
    Projection' method [1]_.

    Parameters
    ----------
    posBottomLeft : list of float or ndarray
        Bottom-left 3D coordinate of the screen in meters.
    posBottomRight : list of float or ndarray
        Bottom-right 3D coordinate of the screen in meters.
    posTopLeft : list of float or ndarray
        Top-left 3D coordinate of the screen in meters.
    eyePos : list of float or ndarray
        Coordinate of the eye in meters.
    nearClip : float
        Near clipping plane distance from viewer in meters.
    farClip : float
        Far clipping plane distance from viewer in meters.
    dtype : dtype or str, optional
        Data type for arrays, can either be 'float32' or 'float64'. If `None` is
        specified, the data type is inferred by `out`. If `out` is not provided,
        the default is 'float64'.

    Returns
    -------
    tuple
        The 4x4 projection and view matrix.

    See Also
    --------
    computeFrustum : Compute frustum parameters.

    Notes
    -----
    * The resulting projection frustums are off-axis relative to the center of
      the display.

    * The returned matrices are row-major. Values are floats with 32-bits
      of precision stored as a contiguous (C-order) array.

    References
    ----------
    .. [1] Kooima, R. (2009). Generalized perspective projection. J. Sch.
       Electron. Eng. Comput. Sci.

    Examples
    --------
    Computing a projection and view matrices for a window::

        projMatrix, viewMatrix = viewtools.generalizedPerspectiveProjection(
            posBottomLeft, posBottomRight, posTopLeft, eyePos)
        # set the window matrices
        win.projectionMatrix = projMatrix
        win.viewMatrix = viewMatrix
        # before rendering
        win.applyEyeTransform()

    Stereo-pair rendering example from Kooima (2009)::

        # configuration of screen and eyes
        posBottomLeft = [-1.5, -0.75, -18.0]
        posBottomRight = [1.5, -0.75, -18.0]
        posTopLeft = [-1.5, 0.75, -18.0]
        posLeftEye = [-1.25, 0.0, 0.0]
        posRightEye = [1.25, 0.0, 0.0]
        # create projection and view matrices
        leftProjMatrix, leftViewMatrix = generalizedPerspectiveProjection(
            posBottomLeft, posBottomRight, posTopLeft, posLeftEye)
        rightProjMatrix, rightViewMatrix = generalizedPerspectiveProjection(
            posBottomLeft, posBottomRight, posTopLeft, posRightEye)

    """
    # get data type of arrays
    dtype = np.float64 if dtype is None else np.dtype(dtype).type

    # convert everything to numpy arrays
    posBottomLeft = np.asarray(posBottomLeft, dtype=dtype)
    posBottomRight = np.asarray(posBottomRight, dtype=dtype)
    posTopLeft = np.asarray(posTopLeft, dtype=dtype)
    eyePos = np.asarray(eyePos, dtype=dtype)

    # orthonormal basis of the screen plane
    vr = posBottomRight - posBottomLeft
    vr /= np.linalg.norm(vr)
    vu = posTopLeft - posBottomLeft
    vu /= np.linalg.norm(vu)
    vn = np.cross(vr, vu)
    vn /= np.linalg.norm(vn)

    # screen corner vectors
    va = posBottomLeft - eyePos
    vb = posBottomRight - eyePos
    vc = posTopLeft - eyePos

    dist = -np.dot(va, vn)
    nearOverDist = nearClip / dist
    left = np.dot(vr, va) * nearOverDist
    right = np.dot(vr, vb) * nearOverDist
    bottom = np.dot(vu, va) * nearOverDist
    top = np.dot(vu, vc) * nearOverDist

    # projection matrix to return
    projMat = perspectiveProjectionMatrix(
        left, right, bottom, top, nearClip, farClip, dtype=dtype)

    # view matrix to return, first compute the rotation component
    rotMat = np.zeros((4, 4), dtype=dtype)
    rotMat[0, :3] = vr
    rotMat[1, :3] = vu
    rotMat[2, :3] = vn
    rotMat[3, 3] = 1.0

    transMat = np.identity(4, dtype=dtype)
    transMat[:3, 3] = -eyePos

    return projMat, np.matmul(rotMat, transMat)


def orthoProjectionMatrix(left, right, bottom, top, nearClip, farClip,
                          out=None, dtype=None):
    """Compute an orthographic projection matrix with provided frustum
    parameters.

    Parameters
    ----------
    left : float
        Left clipping plane coordinate.
    right : float
        Right clipping plane coordinate.
    bottom : float
        Bottom clipping plane coordinate.
    top : float
        Top clipping plane coordinate.
    nearClip : float
        Near clipping plane distance from viewer.
    farClip : float
        Far clipping plane distance from viewer.
    out : ndarray, optional
        Optional output array. Must be same `shape` and `dtype` as the expected
        output if `out` was not specified.
    dtype : dtype or str, optional
        Data type for arrays, can either be 'float32' or 'float64'. If `None` is
        specified, the data type is inferred by `out`. If `out` is not provided,
        the default is 'float64'.

    Returns
    -------
    ndarray
        4x4 projection matrix

    See Also
    --------
    perspectiveProjectionMatrix : Compute a perspective projection matrix.

    Notes
    -----

    * The returned matrix is row-major. Values are floats with 32-bits of
      precision stored as a contiguous (C-order) array.

    """
    if out is None:
        dtype = np.float64 if dtype is None else np.dtype(dtype).type
    else:
        dtype = np.dtype(out.dtype).type

    projMat = np.zeros((4, 4,), dtype=dtype) if out is None else out
    projMat.fill(0.0)

    u = dtype(2.0)
    projMat[0, 0] = u / (right - left)
    projMat[1, 1] = u / (top - bottom)
    projMat[2, 2] = -u / (farClip - nearClip)
    projMat[0, 3] = -((right + left) / (right - left))
    projMat[1, 3] = -((top + bottom) / (top - bottom))
    projMat[2, 3] = -((farClip + nearClip) / (farClip - nearClip))
    projMat[3, 3] = 1.0

    return projMat


def perspectiveProjectionMatrix(left, right, bottom, top, nearClip, farClip,
                                out=None, dtype=None):
    """Compute an perspective projection matrix with provided frustum
    parameters. The frustum can be asymmetric.

    Parameters
    ----------
    left : float
        Left clipping plane coordinate.
    right : float
        Right clipping plane coordinate.
    bottom : float
        Bottom clipping plane coordinate.
    top : float
        Top clipping plane coordinate.
    nearClip : float
        Near clipping plane distance from viewer.
    farClip : float
        Far clipping plane distance from viewer.
    out : ndarray, optional
        Optional output array. Must be same `shape` and `dtype` as the expected
        output if `out` was not specified.
    dtype : dtype or str, optional
        Data type for arrays, can either be 'float32' or 'float64'. If `None` is
        specified, the data type is inferred by `out`. If `out` is not provided,
        the default is 'float64'.

    Returns
    -------
    ndarray
        4x4 projection matrix

    See Also
    --------
    orthoProjectionMatrix : Compute a orthographic projection matrix.

    Notes
    -----

    * The returned matrix is row-major. Values are floats with 32-bits of
      precision stored as a contiguous (C-order) array.

    """
    if out is None:
        dtype = np.float64 if dtype is None else np.dtype(dtype).type
    else:
        dtype = np.dtype(out.dtype).type

    projMat = np.zeros((4, 4,), dtype=dtype) if out is None else out
    projMat.fill(0.0)

    u = dtype(2.0)
    projMat[0, 0] = (u * nearClip) / (right - left)
    projMat[1, 1] = (u * nearClip) / (top - bottom)
    projMat[0, 2] = (right + left) / (right - left)
    projMat[1, 2] = (top + bottom) / (top - bottom)
    projMat[2, 2] = -(farClip + nearClip) / (farClip - nearClip)
    projMat[3, 2] = -1.0
    projMat[2, 3] = -(u * farClip * nearClip) / (farClip - nearClip)

    return projMat


def lookAt(eyePos, centerPos, upVec=(0.0, 1.0, 0.0), out=None, dtype=None):
    """Create a transformation matrix to orient a view towards some point. Based
    on the same algorithm as 'gluLookAt'. This does not generate a projection
    matrix, but rather the matrix to transform the observer's view in the scene.

    For more information see:
    https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml

    Parameters
    ----------
    eyePos : list of float or ndarray
        Eye position in the scene.
    centerPos : list of float or ndarray
        Position of the object center in the scene.
    upVec : list of float or ndarray, optional
        Vector defining the up vector. Default is +Y is up.
    out : ndarray, optional
        Optional output array. Must be same `shape` and `dtype` as the expected
        output if `out` was not specified.
    dtype : dtype or str, optional
        Data type for arrays, can either be 'float32' or 'float64'. If `None` is
        specified, the data type is inferred by `out`. If `out` is not provided,
        the default is 'float64'.

    Returns
    -------
    ndarray
        4x4 view matrix

    Notes
    -----

    * The returned matrix is row-major. Values are floats with 32-bits of
      precision stored as a contiguous (C-order) array.

    """
    if out is None:
        dtype = np.float64 if dtype is None else np.dtype(dtype).type
    else:
        dtype = np.dtype(out.dtype).type

    toReturn = np.zeros((4, 4,), dtype=dtype) if out is None else out
    toReturn.fill(0.0)

    eyePos = np.asarray(eyePos, dtype=dtype)
    centerPos = np.asarray(centerPos, dtype=dtype)
    upVec = np.asarray(upVec, dtype=dtype)

    f = centerPos - eyePos
    f /= np.linalg.norm(f)
    upVec /= np.linalg.norm(upVec)

    s = np.cross(f, upVec)
    u = np.cross(s / np.linalg.norm(s), f)

    rotMat = np.zeros((4, 4), dtype=dtype)
    rotMat[0, :3] = s
    rotMat[1, :3] = u
    rotMat[2, :3] = -f
    rotMat[3, 3] = 1.0

    transMat = np.identity(4, dtype=dtype)
    transMat[:3, 3] = -eyePos

    return np.matmul(rotMat, transMat, out=toReturn)


def pointToNdc(wcsPos, viewMatrix, projectionMatrix, out=None, dtype=None):
    """Map the position of a point in world space to normalized device
    coordinates/space.

    Parameters
    ----------
    wcsPos : tuple, list or ndarray
        Nx3 position vector(s) (xyz) in world space coordinates.
    viewMatrix : ndarray
        4x4 view matrix.
    projectionMatrix : ndarray
        4x4 projection matrix.
    out : ndarray, optional
        Optional output array. Must be same `shape` and `dtype` as the expected
        output if `out` was not specified.
    dtype : dtype or str, optional
        Data type for arrays, can either be 'float32' or 'float64'. If `None` is
        specified, the data type is inferred by `out`. If `out` is not provided,
        the default is 'float64'.

    Returns
    -------
    ndarray
        3x1 vector of normalized device coordinates with type 'float32'

    Notes
    -----

    * The point is not visible, falling outside of the viewing frustum, if the
      returned coordinates fall outside of -1 and 1 along any dimension.

    * In the rare instance the point falls directly on the eye in world
      space where the frustum converges to a point (singularity), the divisor
      will be zero during perspective division. To avoid this, the divisor is
      'bumped' to 1e-5.

    * This function assumes the display area is rectilinear. Any distortion or
      warping applied in normalized device or viewport space is not considered.

    Examples
    --------
    Determine if a point is visible::

        point = (0.0, 0.0, 10.0)  # behind the observer
        ndc = pointToNdc(point, win.viewMatrix, win.projectionMatrix)
        isVisible = not np.any((ndc > 1.0) | (ndc < -1.0))

    Convert NDC to viewport (or pixel) coordinates::

        scrRes = (1920, 1200)
        point = (0.0, 0.0, -5.0)  # forward -5.0 from eye
        x, y, z = pointToNdc(point, win.viewMatrix, win.projectionMatrix)
        pixelX = ((x + 1.0) / 2.0) * scrRes[0])
        pixelY = ((y + 1.0) / 2.0) * scrRes[1])
        # object at point will appear at (pixelX, pixelY)

    """
    if out is None:
        dtype = np.float64 if dtype is None else np.dtype(dtype).type
    else:
        dtype = np.dtype(out.dtype).type

    wcsPos = np.asarray(wcsPos, dtype=dtype)  # convert to array
    toReturn = np.zeros_like(wcsPos, dtype=dtype) if out is None else out

    # forward transform from world to clipping space
    viewProjMatrix = np.zeros((4, 4,), dtype=dtype)
    np.matmul(projectionMatrix, viewMatrix, viewProjMatrix)

    pnts, rtn = np.atleast_2d(wcsPos, toReturn)

    # convert to 4-vector with W=1.0
    wcsVec = np.zeros((pnts.shape[0], 4), dtype=dtype)
    wcsVec[:, :3] = wcsPos
    wcsVec[:, 3] = 1.0

    # convert to homogeneous clip space
    wcsVec = mt.applyMatrix(viewProjMatrix, wcsVec, dtype=dtype)

    # handle the singularity where perspective division will fail
    wcsVec[np.abs(wcsVec[:, 3]) <= np.finfo(dtype).eps] = np.finfo(dtype).eps
    rtn[:, :] = wcsVec[:, :3] / wcsVec[:, 3:]  # xyz / w

    return toReturn


def cursorToRay(cursorX, cursorY, winSize, viewport, projectionMatrix,
                normalize=True, out=None, dtype=None):
    """Convert a 2D mouse coordinate to a 3D ray.

    Takes a 2D window/mouse coordinate and transforms it to a 3D direction
    vector from the viewpoint in eye space (vector origin is [0, 0, 0]). The
    center of the screen projects to vector [0, 0, -1].

    Parameters
    ----------
    cursorX, cursorY :  float or int
        Window coordinates. These need to be scaled if you are using a
        framebuffer that does not have 1:1 pixel mapping (i.e. retina display).
    winSize : array_like
        Size of the window client area [w, h].
    viewport : array_like
        Viewport rectangle [x, y, w, h] being used.
    projectionMatrix : ndarray
        4x4 projection matrix being used.
    normalize : bool
        Normalize the resulting vector.
    out : ndarray, optional
        Optional output array. Must be same `shape` and `dtype` as the expected
        output if `out` was not specified.
    dtype : dtype or str, optional
        Data type for arrays, can either be 'float32' or 'float64'. If `None` is
        specified, the data type is inferred by `out`. If `out` is not provided,
        the default is 'float64'.

    Returns
    -------
    ndarray
        Direction vector (x, y, z).

    Examples
    --------
    Place a 3D stim at the mouse location 5.0 scene units (meters) away::

        # define camera
        camera = RigidBodyPose((-3.0, 5.0, 3.5))
        camera.alignTo((0, 0, 0))

        # in the render loop

        dist = 5.0
        mouseRay = vt.cursorToRay(x, y, win.size, win.viewport, win.projectionMatrix)
        mouseRay *= dist  # scale the vector

        # set the sphere position by transforming vector to world space
        sphere.thePose.pos = camera.transform(mouseRay)

    """
    if out is None:
        dtype = np.float64 if dtype is None else np.dtype(dtype).type
    else:
        dtype = np.dtype(out.dtype).type

    toReturn = np.zeros((3,), dtype=dtype) if out is None else out

    projectionMatrix = np.asarray(projectionMatrix, dtype=dtype)

    # compute the inverse model/view and projection matrix
    invPM = np.linalg.inv(projectionMatrix)

    # transform psychopy mouse coordinates to viewport coordinates
    cursorX = cursorX + (winSize[0] / 2.0)
    cursorY = cursorY + (winSize[1] / 2.0)

    # get the NDC coordinates of the
    projX = 2. * (cursorX - viewport[0]) / viewport[2] - 1.0
    projY = 2. * (cursorY - viewport[1]) / viewport[3] - 1.0

    vecNear = np.array((projX, projY, 0.0, 1.0), dtype=dtype)
    vecFar = np.array((projX, projY, 1.0, 1.0), dtype=dtype)

    vecNear[:] = vecNear.dot(invPM.T)
    vecFar[:] = vecFar.dot(invPM.T)

    vecNear /= vecNear[3]
    vecFar /= vecFar[3]

    # direction vector
    toReturn[:] = (vecFar - vecNear)[:3]

    if normalize:
        mt.normalize(toReturn, out=toReturn)

    return toReturn

